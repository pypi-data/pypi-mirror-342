import os
import re
import sys
import requests
from typing import List
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("addr_risk",log_level='ERROR')  # 这个就是MCP Server的名字
 
@mcp.tool(name="地址转经纬度", description="高德地图API，输入地址，返回地址的经纬度")
def address_to_coordinates(address):
    """
    将地址转换为经纬度
    Args:
        address:地址
    Returns:
        lng:纬度
        lat:经度
    """
    # api_key = os.getenv('api-key', '')
    base_url = "https://apis.map.qq.com/ws/geocoder/v1/"
    base_url='https://apis.map.qq.com/ws/geocoder/v1/?address={}&key={}'.format(address,API_key)
    
    try:
        response = requests.get(base_url)
        result = response.json()
        lng,lat=result['result']['location']['lng'],result['result']['location']['lat']
    except:
        print('未配置api-key，或者调用接口失败')
        lng,lat='',''

    return lng,lat

def run(api_key):
    global API_key
    API_key=api_key
    # 启动MCP服务器
    mcp.run(transport="stdio")

if __name__ == "__main__":
    api_key=sys.argv[1]
    run(api_key)