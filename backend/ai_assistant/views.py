from django.http import JsonResponse
import socket
import re
import os

def get_rag_ip_from_nginx():
    """
    尝试从 Nginx 配置文件中读取动态更新的 RAG_MAC_IP_MARKER IP 地址。
    如果读取失败或在本地开发环境，则回退到默认的 127.0.0.1。
    """
    nginx_conf_path = '/etc/nginx/sites-available/pangliantagege.prod.conf'
    default_ip = '127.0.0.1'
    default_port = 8001
    
    if os.path.exists(nginx_conf_path):
        try:
            with open(nginx_conf_path, 'r') as f:
                content = f.read()
                # 匹配格式: proxy_pass http://xxx.xxx.xxx.xxx:8001; # RAG_MAC_IP_MARKER
                match = re.search(r'proxy_pass\s+http://([^:]+):(\d+);\s*#\s*RAG_MAC_IP_MARKER', content)
                if match:
                    return match.group(1), int(match.group(2))
        except Exception as e:
            print(f"Error reading Nginx conf: {e}")
            
    return default_ip, default_port

def rag_health_check(request):
    """
    Checks if the RAG AI service is reachable.
    """
    target_ip, target_port = get_rag_ip_from_nginx()
    
    is_connected = False
    try:
        sock = socket.create_connection((target_ip, target_port), timeout=2)
        sock.close()
        is_connected = True
    except Exception as e:
        is_connected = False

    if is_connected:
        return JsonResponse({'status': 'ok', 'message': f'RAG service ({target_ip}:{target_port}) is connected'})
    else:
        return JsonResponse({'status': 'error', 'message': f'RAG service ({target_ip}:{target_port}) connection failed'}, status=503)
