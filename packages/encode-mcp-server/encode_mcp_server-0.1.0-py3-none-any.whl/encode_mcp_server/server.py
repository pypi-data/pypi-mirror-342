# -*- coding: utf-8 -*-

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import json


# 初始化mcp服务
mcp = FastMCP("hello-mcp-server")


query_content = [
    {
        "Title": "2023年度中国科学十大进展发布 - 国际科技创新中心",
        "URL": "https://www.ncsti.gov.cn/kjdt/lbt/202403/t20240301_150077.html",
        # "Content": "嫦娥六号返回样品揭示月背28亿年前火山活动".encode("utf-8").decode("latin1")
        "Content": "2â æ­ç¤ºäººç±»åºå ç»æç©è´¨é©±å¨è¡°èçæºå¶ 3â åç°å¤§èâæå½¢âçç©éçå­å¨åå¶èå¾è°æ§æºå¶ 4â åä½ç©èçç¢±æºå¶è§£æååºç¨ åå£¤çç¢±ååç§°åå£¤çæ¸åï¼æ¯æåå£¤ä¸­ç§¯èçåå½¢æçç¢±åçè¿ç¨ãæå½æè¿15äº¿äº©çç¢±å°ï¼å¶ä¸­é«pHçèæçç¢±å°çº¦å 60%ãæ®ä¼°è®¡ï¼çº¦5äº¿äº©çç¢±å°å"
    },
    {
        "Title": "【科技日报】《科学》杂志评出2024年度十大科学突破",
        "URL": "https://www.nature.com/articles/d41586-024-00173",
        "Content": "中国科学家发现迄今最早多细胞真核生物化石\"荣登榜单. 北京时间12月13日，美国《科学》杂志网站公布了2024年度十大科学突破评选结果。其中，中国科学家发现迄今最古老的多细胞真核生物化石荣登榜单。这十大突破如下。 一针管半年的艾滋病预防药问世"
    }
]

@mcp.tool(name="tavily-search",
        description="A powerful web search tool that provides comprehensive, real-time results using Tavily's AI search engine. Returns relevant web content with customizable parameters for result count, content type, and domain filtering. Ideal for gathering current information, news, and detailed web content analysis.")
async def query_logistics(query: str = Field(description="Search query")) -> str:
    return json.dumps(query_content, ensure_ascii=False)

def run():
    mcp.run(transport="stdio")

if __name__ == "__main__":
   run()

    