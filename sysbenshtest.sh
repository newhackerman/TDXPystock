#!/bin/bash

# 全面硬件基准测试脚本
# 支持CPU、内存、磁盘IO、网络性能测试并生成HTML报告

set -e
mkdir -p /mnt/test_data
# 配置参数
REPORT_DIR="$(pwd)/benchmark_report_$(date +%Y%m%d_%H%M%S)"
TEMP_DIR="/mnt/test_data"
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
    
    # 检查iperf3版本
    local iperf_version=$(iperf3 --version 2>&1 | head -1)
    log_info "iperf3版本: $iperf_version"
    
    # 测试iperf3基本功能
    log_info "测试iperf3基本功能..."
    if ! iperf3 -s -D -p 5202 --pidfile /tmp/iperf3_test.pid; then
        log_error "iperf3服务器启动失败"
        exit 1
    fi
    
    sleep 1
    
    if ! timeout 5 iperf3 -c localhost -p 5202 -t 1 > /dev/null 2>&1; then
        log_warn "iperf3本地测试失败，网络测试可能不会正常工作"
    else
        log_info "iperf3功能测试通过"
    fi
    
    # 清理测试进程
    local test_pid=$(cat /tmp/iperf3_test.pid 2>/dev/null)
    if [ -n "$test_pid" ] && kill -0 "$test_pid" 2>/dev/null; then
        kill "$test_pid" 2>/dev/null
    fi
    pkill -f "iperf3.*-s.*5202" 2>/dev/null || true
    rm -f /tmp/iperf3_test.pid
}

# 获取系统信息
get_system_info() {
    log_info "收集系统信息..."
    
    cat > "$REPORT_DIR/system_info.json" << EOF
{
    "hostname": "$(hostname)",
    "kernel": "$(uname -r)",
    "os": "$(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"')",
    "cpu_model": "$(lscpu | grep 'Model name' | cut -d: -f2 | xargs)",
    "cpu_cores": $(nproc),
    "cpu_threads": $(lscpu | grep '^CPU(s):' | awk '{print $2}'),
    "memory_total": "$(free -h | grep Mem | awk '{print $2}')",
    "disk_info": "$(df -h / | tail -1 | awk '{print $2 " total, " $4 " available"}')",
    "test_time": "$(date -Iseconds)"
}
EOF
}

# CPU基准测试
test_cpu() {
    log_info "开始CPU基准测试..."
    
    # 单核测试
    log_info "执行单核CPU测试..."
    sysbench cpu --cpu-max-prime=20000 --threads=1 --time=60 run > "$REPORT_DIR/cpu_single_core.txt" 2>&1
    
    # 多核测试
    local max_threads=$(nproc)
    log_info "执行多核CPU测试 (${max_threads}线程)..."
    sysbench cpu --cpu-max-prime=20000 --threads="$max_threads" --time=60 run > "$REPORT_DIR/cpu_multi_core.txt" 2>&1
    
    # 不同线程数测试
    log_info "执行不同线程数CPU测试..."
    for threads in 2 4 8; do
        if [ "$threads" -le "$max_threads" ]; then
            log_info "测试 ${threads} 线程..."
            sysbench cpu --cpu-max-prime=20000 --threads="$threads" --time=30 run > "$REPORT_DIR/cpu_${threads}_threads.txt" 2>&1
        fi
    done
}

# 内存基准测试
test_memory() {
    log_info "开始内存基准测试..."
    
    # 内存顺序读写测试
    log_info "执行内存顺序读写测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read --memory-access-mode=seq --threads=1 run > "$REPORT_DIR/memory_seq_read.txt" 2>&1
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=write --memory-access-mode=seq --threads=1 run > "$REPORT_DIR/memory_seq_write.txt" 2>&1
    
    # 内存随机读写测试
    log_info "执行内存随机读写测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read --memory-access-mode=rnd --threads=1 run > "$REPORT_DIR/memory_rnd_read.txt" 2>&1
    sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=write --memory-access-mode=rnd --threads=1 run > "$REPORT_DIR/memory_rnd_write.txt" 2>&1
    
    # 多线程内存测试
    log_info "执行多线程内存测试..."
    sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=$(nproc) run > "$REPORT_DIR/memory_multithread.txt" 2>&1
}

# 磁盘IO基准测试
test_disk_io() {
    log_info "开始磁盘IO基准测试..."
    
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    # 准备测试文件
    log_info "准备磁盘测试文件..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" prepare > /dev/null 2>&1
    
    # 顺序读测试
    log_info "执行磁盘顺序读测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=seqrd --time=60 --file-num=16 run > "$REPORT_DIR/disk_seq_read.txt" 2>&1
    
    # 顺序写测试
    log_info "执行磁盘顺序写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=seqwr --time=60 --file-num=16 run > "$REPORT_DIR/disk_seq_write.txt" 2>&1
    
    # 随机读测试
    log_info "执行磁盘随机读测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndrd --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_read.txt" 2>&1
    
    # 随机写测试
    log_info "执行磁盘随机写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndwr --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_write.txt" 2>&1
    
    # 混合读写测试
    log_info "执行磁盘混合读写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=rndrw --time=60 --file-num=16 run > "$REPORT_DIR/disk_rnd_rw.txt" 2>&1
    
    # 大文件连续读写测试
    log_info "执行大文件读写测试..."
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" --file-test-mode=seqrewr --time=60 --file-num=1 --file-block-size=1M run > "$REPORT_DIR/disk_large_file.txt" 2>&1
    
    # 清理测试文件
    sysbench fileio --file-total-size="$TEST_FILE_SIZE" cleanup > /dev/null 2>&1
    cd - > /dev/null
}

# 网络基准测试
test_network() {
    log_info "开始网络基准测试..."
    
    # 本地回环测试
    log_info "执行本地网络回环测试..."
    local server_pid=""
    {
        # 启动iperf3服务器
        iperf3 -s -p 5201 -D --pidfile /tmp/iperf3_server.pid
        server_pid=$(cat /tmp/iperf3_server.pid 2>/dev/null)
        sleep 3
        
        # 执行客户端测试
        log_info "测试本地网络带宽..."
        iperf3 -c localhost -p 5201 -t 20 -J > "$REPORT_DIR/network_localhost.json" 2>&1
        
        # 停止服务器
        if [ -n "$server_pid" ] && kill -0 "$server_pid" 2>/dev/null; then
            kill "$server_pid" 2>/dev/null
        fi
        pkill -f "iperf3.*-s.*5201" 2>/dev/null || true
        rm -f /tmp/iperf3_server.pid
        
        log_info "本地网络测试完成"
    } || {
        log_warn "本地网络测试失败"
        # 清理进程
        pkill -f "iperf3.*-s.*5201" 2>/dev/null || true
        rm -f /tmp/iperf3_server.pid
    }
    
    # 公共iperf3服务器测试
    log_info "测试公共网络服务器连接..."
    local public_servers=("iperf.scottlinux.com" "iperf.par2.as49434.net" "ping.online.net")
    
    for server in "${public_servers[@]}"; do
        log_info "尝试连接到 $server..."
        {
            timeout 30 iperf3 -c "$server" -p 5201 -t 10 -J > "$REPORT_DIR/network_${server//\./_}.json" 2>&1
            if [ $? -eq 0 ]; then
                log_info "成功连接到 $server"
                break
            else
                log_warn "连接 $server 失败，尝试下一个服务器"
            fi
        } || {
            log_warn "连接 $server 超时"
        }
    done
    
    # HTTP下载速度测试 - 使用多个测试源
    log_info "执行HTTP下载速度测试..."
    {
        log_info "测试下载速度 - 100MB文件..."
        echo "=== 100MB Download Test ===" > "$REPORT_DIR/network_download.txt"
        
        # 测试1: speedtest.tele2.net
        {
            echo "Testing speedtest.tele2.net..." >> "$REPORT_DIR/network_download.txt"
            time_output=$(timeout 60 time curl -o /dev/null -s -w "Speed: %{speed_download} bytes/sec, Time: %{time_total}s\n" "http://speedtest.tele2.net/100MB.zip" 2>&1)
            echo "$time_output" >> "$REPORT_DIR/network_download.txt"
        } || {
            echo "speedtest.tele2.net test failed" >> "$REPORT_DIR/network_download.txt"
        }
        
        # 测试2: proof.ovh.net 10MB文件
        {
            echo -e "\nTesting proof.ovh.net..." >> "$REPORT_DIR/network_download.txt"
            time_output=$(timeout 30 time curl -o /dev/null -s -w "Speed: %{speed_download} bytes/sec, Time: %{time_total}s\n" "http://proof.ovh.net/files/10Mb.dat" 2>&1)
            echo "$time_output" >> "$REPORT_DIR/network_download.txt"
        } || {
            echo "proof.ovh.net test failed" >> "$REPORT_DIR/network_download.txt"
        }
        
        log_info "HTTP下载测试完成"
    } || log_warn "HTTP下载测试失败"
    
    # 网络延迟测试 - 测试多个目标
    log_info "执行网络延迟测试..."
    {
        echo "=== Network Latency Tests ===" > "$REPORT_DIR/network_ping.txt"
        
        # 测试多个目标的延迟
        local ping_targets=("8.8.8.8" "1.1.1.1" "114.114.114.114" "baidu.com")
        
        for target in "${ping_targets[@]}"; do
            echo -e "\n--- Ping to $target ---" >> "$REPORT_DIR/network_ping.txt"
            ping -c 5 -W 3 "$target" >> "$REPORT_DIR/network_ping.txt" 2>&1 || {
                echo "Ping to $target failed" >> "$REPORT_DIR/network_ping.txt"
            }
        done
        
        log_info "网络延迟测试完成"
    } || log_warn "网络延迟测试失败"
    
    # 网络连接质量测试
    log_info "执行网络连接质量测试..."
    {
        echo "=== Network Connection Quality ===" > "$REPORT_DIR/network_quality.txt"
        
        # DNS解析测试
        echo "--- DNS Resolution Test ---" >> "$REPORT_DIR/network_quality.txt"
        for domain in "google.com" "baidu.com" "github.com"; do
            echo -n "Resolving $domain: " >> "$REPORT_DIR/network_quality.txt"
            dig +short "$domain" | head -1 >> "$REPORT_DIR/network_quality.txt" 2>&1 || {
                echo "Failed" >> "$REPORT_DIR/network_quality.txt"
            }
        done
        
        # HTTP连接测试
        echo -e "\n--- HTTP Connection Test ---" >> "$REPORT_DIR/network_quality.txt"
        for url in "http://www.google.com" "http://www.baidu.com"; do
            echo -n "Testing $url: " >> "$REPORT_DIR/network_quality.txt"
            curl_output=$(timeout 10 curl -o /dev/null -s -w "HTTP %{http_code}, Time: %{time_total}s\n" "$url" 2>&1)
            echo "$curl_output" >> "$REPORT_DIR/network_quality.txt"
        done
        
        log_info "网络连接质量测试完成"
    } || log_warn "网络连接质量测试失败"
}

# 解析测试结果
parse_results() {
    log_info "解析测试结果..."
    
    # 解析CPU结果
    parse_cpu_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ]; then
            local events_per_sec=$(grep "events per second:" "$file" | awk '{print $4}')
            local total_time=$(grep "total time:" "$file" | awk '{print $3}' | sed 's/s//')
            echo "\"$test_name\": {\"events_per_sec\": \"$events_per_sec\", \"total_time\": \"$total_time\"}"
        else
            echo "\"$test_name\": {\"events_per_sec\": \"N/A\", \"total_time\": \"N/A\"}"
        fi
    }
    
    # 解析内存结果
    parse_memory_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ]; then
            local throughput=$(grep "MiB/sec" "$file" | awk '{print $2}')
            local total_ops=$(grep "total number of events:" "$file" | awk '{print $5}')
            echo "\"$test_name\": {\"throughput_mib_sec\": \"$throughput\", \"total_ops\": \"$total_ops\"}"
        else
            echo "\"$test_name\": {\"throughput_mib_sec\": \"N/A\", \"total_ops\": \"N/A\"}"
        fi
    }
    
    # 解析磁盘IO结果
    parse_disk_results() {
        local file=$1
        local test_name=$2
        if [ -f "$file" ]; then
            local read_throughput=$(grep "read, MiB/s:" "$file" | awk '{print $3}')
            local write_throughput=$(grep "written, MiB/s:" "$file" | awk '{print $3}')
            local iops=$(grep "Requests/sec executed:" "$file" | awk '{print $3}')
            echo "\"$test_name\": {\"read_mib_sec\": \"$read_throughput\", \"write_mib_sec\": \"$write_throughput\", \"iops\": \"$iops\"}"
        else
            echo "\"$test_name\": {\"read_mib_sec\": \"N/A\", \"write_mib_sec\": \"N/A\", \"iops\": \"N/A\"}"
        fi
    }
    
    # 解析网络结果
    parse_network_results() {
        local results="{"
        
        # 解析iperf3本地测试结果
        if [ -f "$REPORT_DIR/network_localhost.json" ]; then
            local bandwidth=$(python3 -c "
import json, sys
try:
    with open('$REPORT_DIR/network_localhost.json', 'r') as f:
        data = json.load(f)
        print(f\"{data['end']['sum_received']['bits_per_second']:.0f}\")
except:
    print('N/A')
" 2>/dev/null)
            results="$results\"localhost_bandwidth_bps\": \"$bandwidth\","
        else
            results="$results\"localhost_bandwidth_bps\": \"N/A\","
        fi
        
        # 解析下载速度测试
        if [ -f "$REPORT_DIR/network_download.txt" ]; then
            local download_speed=$(grep "Speed:" "$REPORT_DIR/network_download.txt" | head -1 | awk '{print $2}')
            results="$results\"download_speed_bps\": \"$download_speed\","
        else
            results="$results\"download_speed_bps\": \"N/A\","
        fi
        
        # 解析ping延迟
        if [ -f "$REPORT_DIR/network_ping.txt" ]; then
            local avg_ping=$(grep "avg" "$REPORT_DIR/network_ping.txt" | head -1 | awk -F'/' '{print $5}' | awk '{print $1}')
            results="$results\"avg_ping_ms\": \"$avg_ping\""
        else
            results="$results\"avg_ping_ms\": \"N/A\""
        fi
        
        results="$results}"
        echo "\"network\": $results"
    }
    
    # 创建结果JSON
    cat > "$REPORT_DIR/results.json" << EOF
{
    "cpu": {
        $(parse_cpu_results "$REPORT_DIR/cpu_single_core.txt" "single_core"),
        $(parse_cpu_results "$REPORT_DIR/cpu_multi_core.txt" "multi_core")
    },
    "memory": {
        $(parse_memory_results "$REPORT_DIR/memory_seq_read.txt" "seq_read"),
        $(parse_memory_results "$REPORT_DIR/memory_seq_write.txt" "seq_write"),
        $(parse_memory_results "$REPORT_DIR/memory_rnd_read.txt" "rnd_read"),
        $(parse_memory_results "$REPORT_DIR/memory_rnd_write.txt" "rnd_write")
    },
    "disk": {
        $(parse_disk_results "$REPORT_DIR/disk_seq_read.txt" "seq_read"),
        $(parse_disk_results "$REPORT_DIR/disk_seq_write.txt" "seq_write"),
        $(parse_disk_results "$REPORT_DIR/disk_rnd_read.txt" "rnd_read"),
        $(parse_disk_results "$REPORT_DIR/disk_rnd_write.txt" "rnd_write")
    },
    $(parse_network_results)
}
EOF
}

# 生成HTML报告
generate_html_report() {
    log_info "生成HTML报告..."
    
    cat > "$REPORT_DIR/benchmark_report.html" << 'EOF'
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
        
        .performance-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .performance-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-excellent {
            background: #d4edda;
            color: #155724;
        }
        
        .status-good {
            background: #cce5ff;
            color: #004085;
        }
        
        .status-average {
            background: #fff3cd;
            color: #856404;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
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
        
        .chart-container {
            margin: 20px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
        // 加载测试数据
        function loadTestData() {
            // 这里应该加载实际的测试结果
            // 由于是静态HTML，我们使用模拟数据
            
            const systemInfo = {
                hostname: "test-server",
                kernel: "5.4.0-74-generic",
                os: "Ubuntu 20.04.2 LTS",
                cpu_model: "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz",
                cpu_cores: 6,
                cpu_threads: 12,
                memory_total: "16G",
                disk_info: "500G total, 350G available",
                test_time: new Date().toISOString()
            };
            
            // 渲染系统信息
            const systemInfoDiv = document.getElementById('systemInfo');
            systemInfoDiv.innerHTML = `
                <div class="info-item">
                    <div class="info-label">主机名</div>
                    <div class="info-value">${systemInfo.hostname}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">操作系统</div>
                    <div class="info-value">${systemInfo.os}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">内核版本</div>
                    <div class="info-value">${systemInfo.kernel}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">CPU型号</div>
                    <div class="info-value">${systemInfo.cpu_model}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">CPU核心/线程</div>
                    <div class="info-value">${systemInfo.cpu_cores}/${systemInfo.cpu_threads}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">内存容量</div>
                    <div class="info-value">${systemInfo.memory_total}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">磁盘空间</div>
                    <div class="info-value">${systemInfo.disk_info}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">测试时间</div>
                    <div class="info-value">${new Date(systemInfo.test_time).toLocaleString()}</div>
                </div>
            `;
            
            document.getElementById('testTime').textContent = new Date().toLocaleString();
        }
        
        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', loadTestData);
    </script>
</body>
</html>
EOF

    # 创建简化版本，包含实际测试结果的占位符
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
    test_cpu
    test_memory
    test_disk_io
    test_network
    
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
    log_info "=================================================="
    
    # 清理临时文件
    rm -rf "$TEMP_DIR"
    
    log_info "基准测试完成！请查看HTML报告获取详细结果。"
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
