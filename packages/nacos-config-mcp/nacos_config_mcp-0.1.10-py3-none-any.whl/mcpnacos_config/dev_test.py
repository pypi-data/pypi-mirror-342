import json
import unittest
import main


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_get_config(self):
        config = await main.get_config(
            server_url="http://dev-integ-env.iflyrec.com:80",
            data_id="YYZX-StoreOrderService.properties",
            username="readonly",
            password="0Jpuhg4n6sTxdYy6",
            group="TJPT",
            namespace_id="integ",
        )
        await self.print_json(config)

    async def print_json(self, payload):
        print(json.dumps(payload, indent=4, ensure_ascii=False))

    async def test_get_configs(self):
        configs = await main.get_configs(
            server_url="http://dev-integ-env.iflyrec.com:80",
            username="readonly",
            password="0Jpuhg4n6sTxdYy6",
            namespace_id="integ",
            page_no=1,
            page_size=1,
        )
        await self.print_json(configs)

if __name__ == "__main__":
    unittest.main()
