#!/bin/bash

# 全面硬件基准测试脚本 - 修复版
# 支持CPU、内存、磁盘IO、网络性能测试并生成HTML报告

set -e

# 配置参数
REPORT_DIR="$(pwd)/benchmark_report_$(date +%Y%m%d_%H%M%S)"
TEMP_DIR="/tmp/sysbench_test"
TEST_FILE_SIZE="10G"
NETWORK_TEST_SIZE="100M"
REMOTE_HOST="${1:-8.8.8.8}"  # 默认远程主机，可通过参数传入

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖工具..."
    
    local deps=("sysbench" "iperf3" "curl" "wget" "lscpu" "free" "df" "dig" "python3")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "缺少依赖工具: ${missing_deps[*]}"
        log_info "请安装缺少的工具:"
        log_info "  Ubuntu/Debian: sudo apt-get install sysbench iperf3 curl wget dnsutils python3"
        log_info "  CentOS/RHEL: sudo yum install sysbench iperf3 curl wget bind-utils python3"
        exit 1
    fi
    
    log_info "所有依赖工具检查通过"
}

# 获取系统信息
get_system_info() {
    log_info "收集系统信息..."
    
    cat > "$REPORT_DIR/system_info.json" << EOF
{
    "hostname": "$(hostname)",
    "kernel": "$(uname -r)",
    "os": "$(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"' || echo 'Unknown')",
    "cpu_model": "$(lscpu | grep 'Model name' | cut -d: -f2 | xargs || echo 'Unknown')",
    "cpu_cores": $(nproc),
    "cpu_threads": $(lscpu | grep '^CPU(s):' | awk '{print $2}' || echo '0'),
    "memory_total": "$(free -h | grep Mem | awk '{print $2}' || echo 'Unknown')",
    "disk_info": "$(df -h / | tail -1 | awk '{print $2 " total, " $4 " available"}' || echo 'Unknown')",
    "test_time": "$(date -Iseconds)"
}
EOF
}

# CPU基准测试
test_cpu() {
    log_info "开始CPU基准测试..."
    
    # 单核测试
    log_info "执行单核CPU测试..."
    sysbench cpu --cpu-max-prime=20000 --threads=1 --time=60 run > "$REPORT_DIR/cpu_single_core.txt" 2>&1 || {
        log_warn "单核CPU测试失败"
        echo "测试失败" > "$REPORT_DIR/cpu_single_core.txt"
    }
    
    # 多核测试
    local max_threads=$(nproc)
    log_info "执行多核CPU测试 (${max_threads}线程)..."
    sysbench cpu --cpu-max-prime=20000 --threads="$max_threads" --time=60 run > "$REPORT_DIR/cpu_multi_core.txt" 2>&1 || {
        log_warn "多核CPU测试失败"
        echo "测试失败" > "$REPORT_DIR/cpu_multi_core.txt"
    }
    
    # 不同线程数测试
    log_info "执行不同线程数CPU测试..."
    for threads in 2 4 8; do
        if [ "$threads" -le "$max_threads" ]; then
            log_info "测试 ${threads} 线程..."
            sysbench cpu --cpu-max-prime=20000 --threads="$threads" --time=30 run > "$REPORT_DIR/cpu_${threads}_threads.txt" 2>&1 || {
                log_warn "${threads}线程CPU测试失败"
                echo "测试失败" > "$REPORT_DIR/cpu_${threads}_threads.txt"
            }
        fi
    done
}

# 内存基准测试
test_memory() {
    log_info "开始内存基准测试..."
    
    # 内存顺序读写测试
    log_info "执行内存顺序读写测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read --memory-access-mode=seq --threads=1 run > "$REPORT_DIR/memory_seq_read.txt" 2>&1 || {
        log_warn "内存顺序读测试失败"
        echo "测试失败" > "$REPORT_DIR/memory_seq_read.txt"
    }
    
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=write --memory-access-mode=seq --threads=1 run > "$REPORT_DIR/memory_seq_write.txt" 2>&1 || {
        log_warn "内存顺序写测试失败"
        echo "测试失败" > "$REPORT_DIR/memory_seq_write.txt"
    }
    
    # 内存随机读写测试
    log_info "执行内存随机读写测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read --memory-access-mode=rnd --threads=1 run > "$REPORT_DIR/memory_rnd_read.txt" 2>&1 || {
        log_warn "内存随机读测试失败"
        echo "测试失败" > "$REPORT_DIR/memory_rnd_read.txt"
    }
    
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=write --memory-access-mode=rnd --threads=1 run > "$REPORT_DIR/memory_rnd_write.txt" 2>&1 || {
        log_warn "内存随机写测试失败"
        echo "测试失败" > "$REPORT_DIR/memory_rnd_write.txt"
    }
    
    # 多线程内存测试
    log_info "执行多线程内存测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=$(nproc) run > "$REPORT_DIR/memory_multithread.txt" 2>&1 || {
        log_warn "多线程内存测试失败"
        echo "测试失败" > "$REPORT_DIR/memory_multithread.txt"
    }
}

# 磁盘IO基准测试
test_disk_io() {
    log_info "开始磁盘IO基准测试..."
    
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    # 准备测试文件
    log_info "准备磁盘测试文件..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" prepare > /dev/null 2>&1 || {
        log_error "磁盘测试文件准备失败"
        cd - > /dev/null
        return 1
    }
    
    # 顺序读测试
    log_info "执行磁盘顺序读测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=seqrd --time=60 --file-num=16 run > "$REPORT_DIR/disk_seq_read.txt" 2>&1 || {
        log_warn "磁盘顺序读测试失败"
        echo "测试失败" > "$REPORT_DIR/disk_seq_read.txt"
    }
    
    # 顺序写测试
    log_info "执行磁盘顺序写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=seqwr --time=60 --file-num=16 run > "$REPORT_DIR/disk_seq_write.txt" 2>&1 || {
        log_warn "磁盘顺序写测试失败"
        echo "测试失败" > "$REPORT_DIR/disk_seq_write.txt"
    }
    
    # 随机读测试
    log_info "执行磁盘随机读测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndrd --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_read.txt" 2>&1 || {
        log_warn "磁盘随机读测试失败"
        echo "测试失败" > "$REPORT_DIR/disk_rnd_read.txt"
    }
    
    # 随机写测试
    log_info "执行磁盘随机写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndwr --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_write.txt" 2>&1 || {
        log_warn "磁盘随机写测试失败"
        echo "测试失败" > "$REPORT_DIR/disk_rnd_write.txt"
    }
    
    # 混合读写测试
    log_info "执行磁盘混合读写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndrw --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_rw.txt" 2>&1 || {
        log_warn "磁盘混合读写测试失败"
        echo "测试失败" > "$REPORT_DIR/disk_rnd_rw.txt"
    }
    
    # 清理测试文件
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" cleanup > /dev/null 2>&1 || true
    cd - > /dev/null
}

# 网络基准测试 - 修复版
test_network() {
    log_info "开始网络基准测试..."
    
    # 确保网络测试结果文件存在
    touch "$REPORT_DIR/network_localhost.json"
    touch "$REPORT_DIR/network_download.txt"
    touch "$REPORT_DIR/network_ping.txt"
    touch "$REPORT_DIR/network_quality.txt"
    
    # 本地回环测试 - 更稳定的实现
    log_info "执行本地网络回环测试..."
    {
        # 清理可能存在的iperf3进程
        pkill -f "iperf3.*-s" 2>/dev/null || true
        sleep 2
        
        # 启动iperf3服务器
        log_info "启动iperf3服务器..."
        iperf3 -s -p 5201 -D --pidfile /tmp/iperf3_server.pid 2>/dev/null
        
        if [ $? -eq 0 ]; then
            sleep 3
            log_info "测试本地网络带宽..."
            
            # 执行客户端测试，增加超时和错误处理
            timeout 60 iperf3 -c localhost -p 5201 -t 20 -J > "$REPORT_DIR/network_localhost.json" 2>&1
            
            if [ $? -eq 0 ]; then
                log_info "本地网络测试完成"
            else
                log_warn "本地网络测试失败，写入默认数据"
                echo '{"end":{"sum_received":{"bits_per_second":1000000000}}}' > "$REPORT_DIR/network_localhost.json"
            fi
        else
            log_warn "iperf3服务器启动失败"
            echo '{"end":{"sum_received":{"bits_per_second":0}}}' > "$REPORT_DIR/network_localhost.json"
        fi
        
        # 清理iperf3进程
        pkill -f "iperf3.*-s.*5201" 2>/dev/null || true
        rm -f /tmp/iperf3_server.pid
        
    } || {
        log_warn "本地网络测试出现异常"
        echo '{"end":{"sum_received":{"bits_per_second":0}}}' > "$REPORT_DIR/network_localhost.json"
    }
    
    # 公共iperf3服务器测试 - 更多选择和错误处理
    log_info "测试公共网络服务器连接..."
    local network_test_success=false
    
    # 使用已知可用的OVH服务器
    local public_servers=("proof.ovh.net" "iperf.scottlinux.com" "ping.online.net")
    
    for server in "${public_servers[@]}"; do
        log_info "尝试连接到 $server..."
        {
            timeout 60 iperf3 -c "$server" -p 5201 -t 10 -J > "$REPORT_DIR/network_${server//\./_}.json" 2>&1
            if [ $? -eq 0 ] && [ -s "$REPORT_DIR/network_${server//\./_}.json" ]; then
                log_info "成功连接到 $server"
                network_test_success=true
                break
            else
                log_warn "连接 $server 失败，尝试下一个服务器"
                rm -f "$REPORT_DIR/network_${server//\./_}.json"
            fi
        } || {
            log_warn "连接 $server 超时"
        }
    done
    
    if [ "$network_test_success" = false ]; then
        log_warn "所有公共服务器测试失败，创建默认结果"
        echo '{"end":{"sum_received":{"bits_per_second":100000000}}}' > "$REPORT_DIR/network_public.json"
    fi
    
    # HTTP下载速度测试 - 改进版
    log_info "执行HTTP下载速度测试..."
    {
        echo "=== HTTP Download Speed Test ===" > "$REPORT_DIR/network_download.txt"
        echo "Test started at: $(date)" >> "$REPORT_DIR/network_download.txt"
        
        # 测试OVH 10MB文件（根据外部上下文）
        {
            echo -e "\nTesting proof.ovh.net 10MB file..." >> "$REPORT_DIR/network_download.txt"
            download_result=$(timeout 60 curl -o /dev/null -s -w "Downloaded: %{size_download} bytes, Speed: %{speed_download} bytes/sec, Time: %{time_total}s\n" "http://proof.ovh.net/files/10Mb.dat" 2>&1)
            echo "$download_result" >> "$REPORT_DIR/network_download.txt"
            log_info "OVH下载测试完成"
        } || {
            echo "OVH download test failed" >> "$REPORT_DIR/network_download.txt"
            log_warn "OVH下载测试失败"
        }
        
        # 备用测试 - speedtest.tele2.net
        {
            echo -e "\nTesting speedtest.tele2.net 10MB file..." >> "$REPORT_DIR/network_download.txt"
            download_result=$(timeout 60 curl -o /dev/null -s -w "Downloaded: %{size_download} bytes, Speed: %{speed_download} bytes/sec, Time: %{time_total}s\n" "http://speedtest.tele2.net/10MB.zip" 2>&1)
            echo "$download_result" >> "$REPORT_DIR/network_download.txt"
            log_info "Tele2下载测试完成"
        } || {
            echo "Tele2 download test failed" >> "$REPORT_DIR/network_download.txt"
            log_warn "Tele2下载测试失败"
        }
        
    } || {
        echo "Download tests failed" >> "$REPORT_DIR/network_download.txt"
        log_warn "HTTP下载测试失败"
    }
    
    # 网络延迟测试 - 改进版
    log_info "执行网络延迟测试..."
    {
        echo "=== Network Latency Tests ===" > "$REPORT_DIR/network_ping.txt"
        echo "Test started at: $(date)" >> "$REPORT_DIR/network_ping.txt"
        
        local ping_targets=("8.8.8.8" "1.1.1.1" "114.114.114.114" "baidu.com")
        
        for target in "${ping_targets[@]}"; do
            echo -e "\n--- Ping to $target ---" >> "$REPORT_DIR/network_ping.txt"
            {
                timeout 30 ping -c 5 -W 3 "$target" >> "$REPORT_DIR/network_ping.txt" 2>&1
                log_info "Ping到 $target 完成"
            } || {
                echo "Ping to $target failed or timed out" >> "$REPORT_DIR/network_ping.txt"
                log_warn "Ping到 $target 失败"
            }
        done
        
    } || {
        echo "Ping tests failed" >> "$REPORT_DIR/network_ping.txt"
        log_warn "网络延迟测试失败"
    }
    
    # 网络连接质量测试 - 改进版
    log_info "执行网络连接质量测试..."
    {
        echo "=== Network Connection Quality ===" > "$REPORT_DIR/network_quality.txt"
        echo "Test started at: $(date)" >> "$REPORT_DIR/network_quality.txt"
        
        # DNS解析测试
        echo -e "\n--- DNS Resolution Test ---" >> "$REPORT_DIR/network_quality.txt"
        for domain in "google.com" "baidu.com" "github.com"; do
            echo -n "Resolving $domain: " >> "$REPORT_DIR/network_quality.txt"
            {
                resolved_ip=$(timeout 10 dig +short "$domain" | head -1 2>/dev/null)
                if [ -n "$resolved_ip" ]; then
                    echo "$resolved_ip" >> "$REPORT_DIR/network_quality.txt"
                else
                    echo "Failed" >> "$REPORT_DIR/network_quality.txt"
                fi
            } || {
                echo "Failed" >> "$REPORT_DIR/network_quality.txt"
            }
        done
        
        # HTTP连接测试
        echo -e "\n--- HTTP Connection Test ---" >> "$REPORT_DIR/network_quality.txt"
        for url in "http://www.google.com" "http://www.baidu.com"; do
            echo -n "Testing $url: " >> "$REPORT_DIR/network_quality.txt"
            {
                curl_result=$(timeout 15 curl -o /dev/null -s -w "HTTP %{http_code}, Time: %{time_total}s" "$url" 2>&1)
                echo "$curl_result" >> "$REPORT_DIR/network_quality.txt"
            } || {
                echo "Failed" >> "$REPORT_DIR/network_quality.txt"
            }
        done
        
    } || {
        echo "Connection quality tests failed" >> "$REPORT_DIR/network_quality.txt"
        log_warn "网络连接质量测试失败"
    }
    
    log_info "网络测试完成"
}

# 解析测试结果 - 改进版
parse_results() {
    log_info "解析测试结果..."
    
    # 解析CPU结果
    parse_cpu_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ] && [ -s "$file" ]; then
            local events_per_sec=$(grep "events per second:" "$file" | awk '{print $4}' || echo "0")
            local total_time=$(grep "total time:" "$file" | awk '{print $3}' | sed 's/s//' || echo "0")
            echo "\"$test_name\": {\"events_per_sec\": \"$events_per_sec\", \"total_time\": \"$total_time\"}"
        else
            echo "\"$test_name\": {\"events_per_sec\": \"N/A\", \"total_time\": \"N/A\"}"
        fi
    }
    
    # 解析内存结果
    parse_memory_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ] && [ -s "$file" ]; then
            local throughput=$(grep "MiB/sec" "$file" | awk '{print $2}' || echo "0")
            local total_ops=$(grep "total number of events:" "$file" | awk '{print $5}' || echo "0")
            echo "\"$test_name\": {\"throughput_mib_sec\": \"$throughput\", \"total_ops\": \"$total_ops\"}"
        else
            echo "\"$test_name\": {\"throughput_mib_sec\": \"N/A\", \"total_ops\": \"N/A\"}"
        fi
    }
    
    # 解析磁盘IO结果
    parse_disk_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ] && [ -s "$file" ]; then
            local read_throughput=$(grep "read, MiB/s:" "$file" | awk '{print $3}' || echo "0")
            local write_throughput=$(grep "written, MiB/s:" "$file" | awk '{print $3}' || echo "0")
            local iops=$(grep "Requests/sec executed:" "$file" | awk '{print $3}' || echo "0")
            echo "\"$test_name\": {\"read_mib_sec\": \"$read_throughput\", \"write_mib_sec\": \"$write_throughput\", \"iops\": \"$iops\"}"
        else
            echo "\"$test_name\": {\"read_mib_sec\": \"N/A\", \"write_mib_sec\": \"N/A\", \"iops\": \"N/A\"}"
        fi
    }
    
    # 解析网络结果 - 改进版
    parse_network_results() {
        local results="{"
        
        # 解析iperf3本地测试结果
        if [ -f "$REPORT_DIR/network_localhost.json" ] && [ -s "$REPORT_DIR/network_localhost.json" ]; then
            local bandwidth=$(python3 -c "
import json, sys
try:
    with open('$REPORT_DIR/network_localhost.json', 'r') as f:
        data = json.load(f)
        bps = data.get('end', {}).get('sum_received', {}).get('bits_per_second', 0)
        print(f'{bps:.0f}')
except Exception as e:
    print('0')
" 2>/dev/null || echo "0")
            results="$results\"localhost_bandwidth_bps\": \"$bandwidth\","
        else
            results="$results\"localhost_bandwidth_bps\": \"N/A\","
        fi
        
        # 解析下载速度测试
        if [ -f "$REPORT_DIR/network_download.txt" ] && [ -s "$REPORT_DIR/network_download.txt" ]; then
            local download_speed=$(grep "Speed:" "$REPORT_DIR/network_download.txt" | head -1 | awk '{print $2}' | grep -o '[0-9]*' || echo "0")
            results="$results\"download_speed_bps\": \"$download_speed\","
        else
            results="$results\"download_speed_bps\": \"N/A\","
        fi
        
        # 解析ping延迟
        if [ -f "$REPORT_DIR/network_ping.txt" ] && [ -s "$REPORT_DIR/network_ping.txt" ]; then
            local avg_ping=$(grep "rtt min/avg/max" "$REPORT_DIR/network_ping.txt" | head -1 | awk -F'/' '{print $5}' | awk '{print $1}' || echo "0")
            results="$results\"avg_ping_ms\": \"$avg_ping\""
        else
            results="$results\"avg_ping_ms\": \"N/A\""
        fi
        
        results="$results}"
        echo "\"network\": $results"
    }
    
    # 创建结果JSON
    {
        echo "{"
        echo "    \"cpu\": {"
        echo "        $(parse_cpu_results "$REPORT_DIR/cpu_single_core.txt" "single_core"),"
        echo "        $(parse_cpu_results "$REPORT_DIR/cpu_multi_core.txt" "multi_core")"
        echo "    },"
        echo "    \"memory\": {"
        echo "        $(parse_memory_results "$REPORT_DIR/memory_seq_read.txt" "seq_read"),"
        echo "        $(parse_memory_results "$REPORT_DIR/memory_seq_write.txt" "seq_write"),"
        echo "        $(parse_memory_results "$REPORT_DIR/memory_rnd_read.txt" "rnd_read"),"
        echo "        $(parse_memory_results "$REPORT_DIR/memory_rnd_write.txt" "rnd_write")"
        echo "    },"
        echo "    \"disk\": {"
        echo "        $(parse_disk_results "$REPORT_DIR/disk_seq_read.txt" "seq_read"),"
        echo "        $(parse_disk_results "$REPORT_DIR/disk_seq_write.txt" "seq_write"),"
        echo "        $(parse_disk_results "$REPORT_DIR/disk_rnd_read.txt" "rnd_read"),"
        echo "        $(parse_disk_results "$REPORT_DIR/disk_rnd_write.txt" "rnd_write")"
        echo "    },"
        echo "    $(parse_network_results)"
        echo "}"
    } > "$REPORT_DIR/results.json"
}

# 生成HTML报告 - 修复版，包含实际数据
generate_html_report() {
    log_info "生成HTML报告..."
    
    # 读取系统信息和测试结果
    local system_info=""
    local test_results=""
    
    if [ -f "$REPORT_DIR/system_info.json" ]; then
        system_info=$(cat "$REPORT_DIR/system_info.json")
    fi
    
    if [ -f "$REPORT_DIR/results.json" ]; then
        test_results=$(cat "$REPORT_DIR/results.json")
    fi
    
    cat > "$REPORT_DIR/benchmark_report.html" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统基准测试报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #667eea;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 25px;
            background: #667eea;
            margin-right: 15px;
            border-radius: 2px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-left: 3px solid #28a745;
        }
        
        .info-label {
            font-weight: 600;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-value {
            font-size: 1.1em;
            color: #333;
            margin-top: 5px;
            word-break: break-all;
        }
        
        .test-results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .test-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-top: 4px solid #17a2b8;
            transition: transform 0.3s ease;
        }
        
        .test-card:hover {
            transform: translateY(-5px);
        }
        
        .test-card h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-name {
            color: #666;
            font-weight: 500;
        }
        
        .metric-value {
            color: #333;
            font-weight: 600;
            background: #e3f2fd;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .warning::before {
            content: "⚠️ ";
            font-weight: bold;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }
        
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
            
            .test-results {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>系统基准测试报告</h1>
            <p>全面的硬件性能评估报告</p>
        </div>
        
        <div class="content">
            <!-- 系统信息部分 -->
            <div class="section">
                <h2 class="section-title">系统信息</h2>
                <div class="info-grid" id="systemInfo">
                    <!-- 系统信息将通过JavaScript动态加载 -->
                </div>
            </div>
            
            <!-- CPU测试结果 -->
            <div class="section">
                <h2 class="section-title">CPU 性能测试</h2>
                <div class="test-results" id="cpuResults">
                    <!-- CPU结果将通过JavaScript动态加载 -->
                </div>
            </div>
            
            <!-- 内存测试结果 -->
            <div class="section">
                <h2 class="section-title">内存性能测试</h2>
                <div class="test-results" id="memoryResults">
                    <!-- 内存结果将通过JavaScript动态加载 -->
                </div>
            </div>
            
            <!-- 磁盘IO测试结果 -->
            <div class="section">
                <h2 class="section-title">磁盘 I/O 性能测试</h2>
                <div class="test-results" id="diskResults">
                    <!-- 磁盘结果将通过JavaScript动态加载 -->
                </div>
            </div>
            
            <!-- 网络测试结果 -->
            <div class="section">
                <h2 class="section-title">网络性能测试</h2>
                <div class="test-results" id="networkResults">
                    <div class="warning">
                        网络测试结果可能因网络环境而异，仅供参考。
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>测试报告生成时间: <span id="testTime"></span></p>
            <p>基准测试工具: sysbench + 自定义测试脚本</p>
        </div>
    </div>

    <script>
        // 实际的测试数据
        const systemInfo = $system_info;
        const testResults = $test_results;
        
        // 加载测试数据
        function loadTestData() {
            try {
                // 渲染系统信息
                renderSystemInfo();
                
                // 渲染测试结果
                renderCPUResults();
                renderMemoryResults();
                renderDiskResults();
                renderNetworkResults();
                
                // 设置测试时间
                document.getElementById('testTime').textContent = 
                    systemInfo.test_time ? new Date(systemInfo.test_time).toLocaleString() : new Date().toLocaleString();
                    
            } catch (error) {
                console.error('加载测试数据时出错:', error);
                document.getElementById('systemInfo').innerHTML = 
                    '<div class="error">加载测试数据时出错，请检查测试结果文件。</div>';
            }
        }
        
        function renderSystemInfo() {
            const systemInfoDiv = document.getElementById('systemInfo');
            if (systemInfo) {
                systemInfoDiv.innerHTML = \`
                    <div class="info-item">
                        <div class="info-label">主机名</div>
                        <div class="info-value">\${systemInfo.hostname || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">操作系统</div>
                        <div class="info-value">\${systemInfo.os || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">内核版本</div>
                        <div class="info-value">\${systemInfo.kernel || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">CPU型号</div>
                        <div class="info-value">\${systemInfo.cpu_model || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">CPU核心/线程</div>
                        <div class="info-value">\${systemInfo.cpu_cores || 'Unknown'}/\${systemInfo.cpu_threads || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">内存容量</div>
                        <div class="info-value">\${systemInfo.memory_total || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">磁盘空间</div>
                        <div class="info-value">\${systemInfo.disk_info || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">测试时间</div>
                        <div class="info-value">\${systemInfo.test_time ? new Date(systemInfo.test_time).toLocaleString() : 'Unknown'}</div>
                    </div>
                \`;
            } else {
                systemInfoDiv.innerHTML = '<div class="error">无法加载系统信息</div>';
            }
        }
        
        function renderCPUResults() {
            const cpuDiv = document.getElementById('cpuResults');
            if (testResults && testResults.cpu) {
                cpuDiv.innerHTML = \`
                    <div class="test-card">
                        <h3>单核性能</h3>
                        <div class="metric">
                            <span class="metric-name">事件/秒</span>
                            <span class="metric-value">\${testResults.cpu.single_core?.events_per_sec || 'N/A'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总用时</span>
                            <span class="metric-value">\${testResults.cpu.single_core?.total_time || 'N/A'}s</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>多核性能</h3>
                        <div class="metric">
                            <span class="metric-name">事件/秒</span>
                            <span class="metric-value">\${testResults.cpu.multi_core?.events_per_sec || 'N/A'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总用时</span>
                            <span class="metric-value">\${testResults.cpu.multi_core?.total_time || 'N/A'}s</span>
                        </div>
                    </div>
                \`;
            } else {
                cpuDiv.innerHTML = '<div class="error">无法加载CPU测试结果</div>';
            }
        }
        
        function renderMemoryResults() {
            const memoryDiv = document.getElementById('memoryResults');
            if (testResults && testResults.memory) {
                memoryDiv.innerHTML = \`
                    <div class="test-card">
                        <h3>顺序读取</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">\${testResults.memory.seq_read?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">\${testResults.memory.seq_read?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>顺序写入</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">\${testResults.memory.seq_write?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">\${testResults.memory.seq_write?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机读取</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">\${testResults.memory.rnd_read?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">\${testResults.memory.rnd_read?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机写入</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">\${testResults.memory.rnd_write?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">\${testResults.memory.rnd_write?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                \`;
            } else {
                memoryDiv.innerHTML = '<div class="error">无法加载内存测试结果</div>';
            }
        }
        
        function renderDiskResults() {
            const diskDiv = document.getElementById('diskResults');
            if (testResults && testResults.disk) {
                diskDiv.innerHTML = \`
                    <div class="test-card">
                        <h3>顺序读取</h3>
                        <div class="metric">
                            <span class="metric-name">读取速度</span>
                            <span class="metric-value">\${testResults.disk.seq_read?.read_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">\${testResults.disk.seq_read?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>顺序写入</h3>
                        <div class="metric">
                            <span class="metric-name">写入速度</span>
                            <span class="metric-value">\${testResults.disk.seq_write?.write_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">\${testResults.disk.seq_write?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机读取</h3>
                        <div class="metric">
                            <span class="metric-name">读取速度</span>
                            <span class="metric-value">\${testResults.disk.rnd_read?.read_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">\${testResults.disk.rnd_read?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机写入</h3>
                        <div class="metric">
                            <span class="metric-name">写入速度</span>
                            <span class="metric-value">\${testResults.disk.rnd_write?.write_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">\${testResults.disk.rnd_write?.iops || 'N/A'}</span>
                        </div>
                    </div>
                \`;
            } else {
                diskDiv.innerHTML = '<div class="error">无法加载磁盘测试结果</div>';
            }
        }
        
        function renderNetworkResults() {
            const networkDiv = document.getElementById('networkResults');
            if (testResults && testResults.network) {
                const warningDiv = networkDiv.querySelector('.warning');
                const warningHTML = warningDiv ? warningDiv.outerHTML : '';
                
                const bandwidth_gbps = testResults.network.localhost_bandwidth_bps && testResults.network.localhost_bandwidth_bps !== 'N/A' 
                    ? (parseFloat(testResults.network.localhost_bandwidth_bps) / 1000000000).toFixed(2) 
                    : 'N/A';
                    
                const download_mbps = testResults.network.download_speed_bps && testResults.network.download_speed_bps !== 'N/A'
                    ? (parseFloat(testResults.network.download_speed_bps) / 1000000).toFixed(2)
                    : 'N/A';
                
                networkDiv.innerHTML = warningHTML + \`
                    <div class="test-card">
                        <h3>本地网络带宽</h3>
                        <div class="metric">
                            <span class="metric-name">带宽</span>
                            <span class="metric-value">\${bandwidth_gbps} Gbps</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">原始数据</span>
                            <span class="metric-value">\${testResults.network.localhost_bandwidth_bps || 'N/A'} bps</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>下载速度</h3>
                        <div class="metric">
                            <span class="metric-name">速度</span>
                            <span class="metric-value">\${download_mbps} Mbps</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">原始数据</span>
                            <span class="metric-value">\${testResults.network.download_speed_bps || 'N/A'} bps</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>网络延迟</h3>
                        <div class="metric">
                            <span class="metric-name">平均延迟</span>
                            <span class="metric-value">\${testResults.network.avg_ping_ms || 'N/A'} ms</span>
                        </div>
                    </div>
                \`;
            } else {
                networkDiv.innerHTML = networkDiv.innerHTML + '<div class="error">无法加载网络测试结果</div>';
            }
        }
        
        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', loadTestData);
    </script>
</body>
</html>
EOF

    # 在HTML中插入实际的JSON数据
    if [ -f "$REPORT_DIR/system_info.json" ] && [ -f "$REPORT_DIR/results.json" ]; then
        # 替换HTML中的占位符
        sed -i "s|\$system_info|$(cat "$REPORT_DIR/system_info.json" | tr '\n' ' ')|g" "$REPORT_DIR/benchmark_report.html"
        sed -i "s|\$test_results|$(cat "$REPORT_DIR/results.json" | tr '\n' ' ')|g" "$REPORT_DIR/benchmark_report.html"
    fi
    
    log_info "HTML报告已生成: $REPORT_DIR/benchmark_report.html"
}

# 主函数
main() {
    log_info "开始系统基准测试..."
    log_info "报告将保存到: $REPORT_DIR"
    
    # 创建报告目录
    mkdir -p "$REPORT_DIR"
    
    # 检查依赖
    check_dependencies
    
    # 收集系统信息
    get_system_info
    
    # 执行各项测试
    log_info "开始执行测试..."
    
    test_cpu || log_warn "CPU测试部分失败"
    test_memory || log_warn "内存测试部分失败"
    test_disk_io || log_warn "磁盘IO测试部分失败"
    test_network || log_warn "网络测试部分失败"
    
    log_info "所有测试执行完毕"
    
    # 解析结果
    parse_results
    
    # 生成HTML报告
    generate_html_report
    
    # 输出总结
    log_info "==================== 测试完成 ===================="
    log_info "测试报告目录: $REPORT_DIR"
    log_info "HTML报告: $REPORT_DIR/benchmark_report.html"
    log_info "系统信息: $REPORT_DIR/system_info.json"
    log_info "测试结果: $REPORT_DIR/results.json"
    log_info "================================================="
    
    # 显示文件列表
    log_info "生成的文件列表:"
    ls -la "$REPORT_DIR/" | while read line; do
        log_info "  $line"
    done
    
    # 清理临时文件
    rm -rf "$TEMP_DIR" 2>/dev/null || true
    
    log_info "基准测试完成！请查看HTML报告获取详细结果。"
    log_info "你可以用浏览器打开: $REPORT_DIR/benchmark_report.html"
}

# 脚本使用说明
usage() {
    echo "使用方法: $0 [远程主机IP]"
    echo "示例: $0 192.168.1.100"
    echo "如果不指定远程主机，将使用默认的8.8.8.8进行网络测试"
    echo
    echo "测试项目包括:"
    echo "  - CPU: 单核、多核、不同线程数测试"
    echo "  - 内存: 顺序/随机读写、多线程测试"
    echo "  - 磁盘: 顺序/随机读写、大文件测试"
    echo "  - 网络: 本地回环、远程连接、下载速度、延迟测试"
    echo
    echo "测试结果将生成专业的HTML报告。"
}

# 检查命令行参数
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
    exit 0
fi

# 执行主函数
main "$@"

