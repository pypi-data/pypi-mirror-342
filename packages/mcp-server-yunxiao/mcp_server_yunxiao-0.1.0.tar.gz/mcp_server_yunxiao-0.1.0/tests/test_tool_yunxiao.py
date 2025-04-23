"""
云霄服务工具测试模块
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tool_yunxiao import (
    describe_sale_policies,
    describe_inventory,
    get_user_owned_grid,
    get_customer_account_info,
    query_quota,
    query_instance_families,
    get_instance_count,
    query_instances,
    get_instance_details
)

class TestToolYunxiao(unittest.TestCase):
    """云霄服务工具测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 设置环境变量
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = ""
        os.environ["YUNXIAO_SECRET_KEY"] = ""
        
    def test_describe_sale_policies(self):
        """测试查询售卖推荐数据"""
        result = describe_sale_policies()
        data = json.loads(result)
        print(data)
        
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)
        
        if data["data"]:
            item = data["data"][0]
            self.assertIn("境内外", item)
            self.assertIn("可用区名称", item)
            self.assertIn("实例族", item)
            self.assertIn("售卖状态", item)
            
    def test_describe_inventory(self):
        """测试查询库存数据"""
        result = describe_inventory(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)
        
        if data["data"]:
            item = data["data"][0]
            self.assertIn("可用区", item)
            self.assertIn("实例族", item)
            self.assertIn("实例类型", item)
            self.assertIn("库存", item)
            
    def test_get_user_owned_grid(self):
        """测试获取用户归属预扣统计"""
        result = get_user_owned_grid(app_id=251000022)
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_customer_account_info(self):
        """测试获取客户账号信息"""
        result = get_customer_account_info(customer_ids=["251000022"])
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_quota(self):
        """测试查询配额信息"""
        result = query_quota(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_instance_families(self):
        """测试查询实例族信息"""
        result = query_instance_families()
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_instance_count(self):
        """测试获取实例数量统计"""
        result = get_instance_count(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_instances(self):
        """测试查询实例列表"""
        result = query_instances(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_instance_details(self):
        """测试获取实例详细信息"""
        result = get_instance_details(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)

if __name__ == "__main__":
    unittest.main() 