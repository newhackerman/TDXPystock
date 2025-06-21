#!/bin/bash

# 修复HTML报告脚本
# 用于修复已生成的基准测试报告中的数据解析问题

set -e

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <报告目录路径>"
    echo "示例: $0 E:/test/benchmark_report_20250609_220339"
    exit 1
fi

REPORT_DIR="$1"

# 检查目录是否存在
if [ ! -d "$REPORT_DIR" ]; then
    echo "错误: 目录 $REPORT_DIR 不存在"
    exit 1
fi

echo "修复报告目录: $REPORT_DIR"

# 改进的解析函数
parse_cpu_results() {
    local file="$1"
    local test_name="$2"
    if [ -f "$file" ] && [ -s "$file" ] && ! grep -q "测试失败" "$file"; then
        local events_per_sec=$(grep "events per second:" "$file" | awk '{print $4}' 2>/dev/null || echo "N/A")
        local total_time=$(grep "total time:" "$file" | awk '{print $3}' | sed 's/s$//' 2>/dev/null || echo "N/A")
        echo "\"$test_name\": {\"events_per_sec\": \"$events_per_sec\", \"total_time\": \"$total_time\"}"
    else
        echo "\"$test_name\": {\"events_per_sec\": \"N/A\", \"total_time\": \"N/A\"}"
    fi
}

parse_memory_results() {
    local file="$1"
    local test_name="$2"
    if [ -f "$file" ] && [ -s "$file" ] && ! grep -q "测试失败" "$file"; then
        # 查找 "MiB transferred (xxx MiB/sec)" 模式
        local throughput=$(grep "MiB transferred" "$file" | sed -n 's/.*transferred (\([0-9.]*\) MiB\/sec).*/\1/p' 2>/dev/null || echo "N/A")
        local total_ops=$(grep "Total operations:" "$file" | awk '{print $3}' 2>/dev/null || echo "N/A")
        echo "\"$test_name\": {\"throughput_mib_sec\": \"$throughput\", \"total_ops\": \"$total_ops\"}"
    else
        echo "\"$test_name\": {\"throughput_mib_sec\": \"N/A\", \"total_ops\": \"N/A\"}"
    fi
}

parse_disk_results() {
    local file="$1"
    local test_name="$2"
    if [ -f "$file" ] && [ -s "$file" ] && ! grep -q "测试失败" "$file"; then
        local read_throughput=$(grep "read, MiB/s:" "$file" | awk '{print $3}' 2>/dev/null || echo "N/A")
        local write_throughput=$(grep "written, MiB/s:" "$file" | awk '{print $3}' 2>/dev/null || echo "N/A")
        local iops=$(grep "Requests/sec executed:" "$file" | awk '{print $3}' 2>/dev/null || echo "N/A")
        # 如果没有找到标准格式，尝试其他格式
        if [ "$read_throughput" = "N/A" ] && [ "$write_throughput" = "N/A" ]; then
            read_throughput=$(grep "Read" "$file" | grep "MiB/s" | awk '{print $2}' 2>/dev/null || echo "N/A")
            write_throughput=$(grep "Written" "$file" | grep "MiB/s" | awk '{print $2}' 2>/dev/null || echo "N/A")
        fi
        echo "\"$test_name\": {\"read_mib_sec\": \"$read_throughput\", \"write_mib_sec\": \"$write_throughput\", \"iops\": \"$iops\"}"
    else
        echo "\"$test_name\": {\"read_mib_sec\": \"N/A\", \"write_mib_sec\": \"N/A\", \"iops\": \"N/A\"}"
    fi
}

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
        local download_speed=$(grep "Speed:" "$REPORT_DIR/network_download.txt" | head -1 | awk '{print $2}' | grep -o '[0-9]*' 2>/dev/null || echo "0")
        results="$results\"download_speed_bps\": \"$download_speed\","
    else
        results="$results\"download_speed_bps\": \"N/A\","
    fi
    
    # 解析ping延迟
    if [ -f "$REPORT_DIR/network_ping.txt" ] && [ -s "$REPORT_DIR/network_ping.txt" ]; then
        local avg_ping=$(grep "rtt min/avg/max" "$REPORT_DIR/network_ping.txt" | head -1 | awk -F'/' '{print $5}' | awk '{print $1}' 2>/dev/null || echo "N/A")
        results="$results\"avg_ping_ms\": \"$avg_ping\""
    else
        results="$results\"avg_ping_ms\": \"N/A\""
    fi
    
    results="$results}"
    echo "\"network\": $results"
}

# 重新解析测试结果
echo "重新解析测试结果..."
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
} > "$REPORT_DIR/results_fixed.json"

# 修复system_info.json
echo "修复系统信息..."
if [ -f "$REPORT_DIR/system_info.json" ]; then
    # 修复JSON语法错误
    sed 's/"cpu_threads": ,/"cpu_threads": "Unknown",/g' "$REPORT_DIR/system_info.json" | \
    sed 's/"memory_total": "",/"memory_total": "Unknown",/g' > "$REPORT_DIR/system_info_fixed.json"
else
    echo "系统信息文件不存在"
    exit 1
fi

# 生成修复的HTML报告
echo "生成修复的HTML报告..."
cat > "$REPORT_DIR/benchmark_report_fixed.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统基准测试报告 - 修复版</title>
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
        
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
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
            <p>全面的硬件性能评估报告 - 修复版</p>
        </div>
        
        <div class="content">
            <div class="success">
                ✅ 此版本已修复数据解析问题，显示完整的测试结果。
            </div>
            
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
            <p>基准测试工具: sysbench + 自定义测试脚本 (修复版)</p>
        </div>
    </div>

    <script>
        // 加载修复后的测试数据
        let systemInfo = {};
        let testResults = {};
        
        // 异步加载JSON数据
        async function loadJSONData() {
            try {
                // 这里我们将直接嵌入数据
                systemInfo = SYSTEM_INFO_PLACEHOLDER;
                testResults = TEST_RESULTS_PLACEHOLDER;
                return true;
            } catch (error) {
                console.error('加载JSON数据失败:', error);
                return false;
            }
        }
        
        function renderSystemInfo() {
            const systemInfoDiv = document.getElementById('systemInfo');
            if (systemInfo && Object.keys(systemInfo).length > 0) {
                systemInfoDiv.innerHTML = `
                    <div class="info-item">
                        <div class="info-label">主机名</div>
                        <div class="info-value">${systemInfo.hostname || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">操作系统</div>
                        <div class="info-value">${systemInfo.os || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">内核版本</div>
                        <div class="info-value">${systemInfo.kernel || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">CPU型号</div>
                        <div class="info-value">${systemInfo.cpu_model || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">CPU核心/线程</div>
                        <div class="info-value">${systemInfo.cpu_cores || 'Unknown'}/${systemInfo.cpu_threads || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">内存容量</div>
                        <div class="info-value">${systemInfo.memory_total || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">磁盘空间</div>
                        <div class="info-value">${systemInfo.disk_info || 'Unknown'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">测试时间</div>
                        <div class="info-value">${systemInfo.test_time ? new Date(systemInfo.test_time).toLocaleString() : 'Unknown'}</div>
                    </div>
                `;
            } else {
                systemInfoDiv.innerHTML = '<div class="error">无法加载系统信息</div>';
            }
        }
        
        function renderCPUResults() {
            const cpuDiv = document.getElementById('cpuResults');
            if (testResults && testResults.cpu) {
                cpuDiv.innerHTML = `
                    <div class="test-card">
                        <h3>单核性能</h3>
                        <div class="metric">
                            <span class="metric-name">事件/秒</span>
                            <span class="metric-value">${testResults.cpu.single_core?.events_per_sec || 'N/A'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总用时</span>
                            <span class="metric-value">${testResults.cpu.single_core?.total_time || 'N/A'}s</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>多核性能</h3>
                        <div class="metric">
                            <span class="metric-name">事件/秒</span>
                            <span class="metric-value">${testResults.cpu.multi_core?.events_per_sec || 'N/A'}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总用时</span>
                            <span class="metric-value">${testResults.cpu.multi_core?.total_time || 'N/A'}s</span>
                        </div>
                    </div>
                `;
            } else {
                cpuDiv.innerHTML = '<div class="error">无法加载CPU测试结果</div>';
            }
        }
        
        function renderMemoryResults() {
            const memoryDiv = document.getElementById('memoryResults');
            if (testResults && testResults.memory) {
                memoryDiv.innerHTML = `
                    <div class="test-card">
                        <h3>顺序读取</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">${testResults.memory.seq_read?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">${testResults.memory.seq_read?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>顺序写入</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">${testResults.memory.seq_write?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">${testResults.memory.seq_write?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机读取</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">${testResults.memory.rnd_read?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">${testResults.memory.rnd_read?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机写入</h3>
                        <div class="metric">
                            <span class="metric-name">吞吐量</span>
                            <span class="metric-value">${testResults.memory.rnd_write?.throughput_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">总操作数</span>
                            <span class="metric-value">${testResults.memory.rnd_write?.total_ops || 'N/A'}</span>
                        </div>
                    </div>
                `;
            } else {
                memoryDiv.innerHTML = '<div class="error">无法加载内存测试结果</div>';
            }
        }
        
        function renderDiskResults() {
            const diskDiv = document.getElementById('diskResults');
            if (testResults && testResults.disk) {
                diskDiv.innerHTML = `
                    <div class="test-card">
                        <h3>顺序读取</h3>
                        <div class="metric">
                            <span class="metric-name">读取速度</span>
                            <span class="metric-value">${testResults.disk.seq_read?.read_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">${testResults.disk.seq_read?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>顺序写入</h3>
                        <div class="metric">
                            <span class="metric-name">写入速度</span>
                            <span class="metric-value">${testResults.disk.seq_write?.write_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">${testResults.disk.seq_write?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机读取</h3>
                        <div class="metric">
                            <span class="metric-name">读取速度</span>
                            <span class="metric-value">${testResults.disk.rnd_read?.read_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">${testResults.disk.rnd_read?.iops || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>随机写入</h3>
                        <div class="metric">
                            <span class="metric-name">写入速度</span>
                            <span class="metric-value">${testResults.disk.rnd_write?.write_mib_sec || 'N/A'} MiB/s</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">IOPS</span>
                            <span class="metric-value">${testResults.disk.rnd_write?.iops || 'N/A'}</span>
                        </div>
                    </div>
                `;
            } else {
                diskDiv.innerHTML = '<div class="error">无法加载磁盘测试结果</div>';
            }
        }
        
        function renderNetworkResults() {
            const networkDiv = document.getElementById('networkResults');
            if (testResults && testResults.network) {
                const warningDiv = networkDiv.querySelector('.warning');
                const warningHTML = warningDiv ? warningDiv.outerHTML : '';
                
                const bandwidth_gbps = testResults.network.localhost_bandwidth_bps && 
                                     testResults.network.localhost_bandwidth_bps !== 'N/A' && 
                                     testResults.network.localhost_bandwidth_bps !== '0'
                    ? (parseFloat(testResults.network.localhost_bandwidth_bps) / 1000000000).toFixed(2) 
                    : 'N/A';
                    
                const download_mbps = testResults.network.download_speed_bps && 
                                    testResults.network.download_speed_bps !== 'N/A' && 
                                    testResults.network.download_speed_bps !== '0'
                    ? (parseFloat(testResults.network.download_speed_bps) / 1000000).toFixed(2)
                    : 'N/A';
                
                networkDiv.innerHTML = warningHTML + `
                    <div class="test-card">
                        <h3>本地网络带宽</h3>
                        <div class="metric">
                            <span class="metric-name">带宽</span>
                            <span class="metric-value">${bandwidth_gbps} Gbps</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">原始数据</span>
                            <span class="metric-value">${testResults.network.localhost_bandwidth_bps || 'N/A'} bps</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>下载速度</h3>
                        <div class="metric">
                            <span class="metric-name">速度</span>
                            <span class="metric-value">${download_mbps} Mbps</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">原始数据</span>
                            <span class="metric-value">${testResults.network.download_speed_bps || 'N/A'} bps</span>
                        </div>
                    </div>
                    <div class="test-card">
                        <h3>网络延迟</h3>
                        <div class="metric">
                            <span class="metric-name">平均延迟</span>
                            <span class="metric-value">${testResults.network.avg_ping_ms || 'N/A'} ms</span>
                        </div>
                    </div>
                `;
            } else {
                networkDiv.innerHTML = networkDiv.innerHTML + '<div class="error">无法加载网络测试结果</div>';
            }
        }
        
        // 主加载函数
        async function loadTestData() {
            try {
                const dataLoaded = await loadJSONData();
                if (dataLoaded) {
                    renderSystemInfo();
                    renderCPUResults();
                    renderMemoryResults();
                    renderDiskResults();
                    renderNetworkResults();
                    
                    document.getElementById('testTime').textContent = 
                        systemInfo.test_time ? new Date(systemInfo.test_time).toLocaleString() : new Date().toLocaleString();
                } else {
                    throw new Error('数据加载失败');
                }
            } catch (error) {
                console.error('加载测试数据时出错:', error);
                document.getElementById('systemInfo').innerHTML = 
                    '<div class="error">加载测试数据时出错，请检查测试结果文件。</div>';
            }
        }
        
        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', loadTestData);
    </script>
</body>
</html>
EOF

# 在HTML中插入实际的JSON数据
if [ -f "$REPORT_DIR/system_info_fixed.json" ] && [ -f "$REPORT_DIR/results_fixed.json" ]; then
    # 读取JSON数据并替换占位符
    system_info_data=$(cat "$REPORT_DIR/system_info_fixed.json" | tr '\n' ' ')
    test_results_data=$(cat "$REPORT_DIR/results_fixed.json" | tr '\n' ' ')
    
    # 替换HTML中的占位符
    sed -i "s|SYSTEM_INFO_PLACEHOLDER|$system_info_data|g" "$REPORT_DIR/benchmark_report_fixed.html"
    sed -i "s|TEST_RESULTS_PLACEHOLDER|$test_results_data|g" "$REPORT_DIR/benchmark_report_fixed.html"
    
    echo "修复完成！"
    echo "修复后的文件:"
    echo "  - 系统信息: $REPORT_DIR/system_info_fixed.json"
    echo "  - 测试结果: $REPORT_DIR/results_fixed.json"
    echo "  - HTML报告: $REPORT_DIR/benchmark_report_fixed.html"
    echo ""
    echo "请用浏览器打开修复后的HTML报告查看完整数据。"
else
    echo "错误: 无法创建修复的JSON文件"
    exit 1
fi

