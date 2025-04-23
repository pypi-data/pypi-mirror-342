#!/usr/bin/env python3
import argparse
import logging
import os
from pydoc import describe
from typing import Dict, Optional

import volcenginesdkcore
import volcenginesdkstorageebs

from .config import load_config
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variables
storage_ebs_service = None

# Create MCP server
mcp = FastMCP("Storage EBS MCP Server", port=int(os.getenv("PORT", "8000")))



@mcp.tool()
def describe_volume(
    volume_id: Optional[str] = None,
    instance_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Query information about a specific EBS volume.
    This tool retrieves details of an EBS volume including status, size, creation time etc.

    Args:
        volume_id: The ID of the EBS volume id to query (e.g. "vol-12345678")
        instance_id: The ID of the instance associated with the volume (e.g. "i-12345678")
        query: Optional specific questions about the volume(status, size, creation time etc.)
    """
    logger.info(f"Received describe_volume request for volume: {volume_id}")

    try:
        volumes_ids = []
        if volume_id is not None:
            volumes_ids = [volume_id]
        describe_request = volcenginesdkstorageebs.DescribeVolumesRequest(
            volume_ids=volumes_ids,
            instance_id=instance_id
        )
        describe_response = ebs_cli.describe_volumes(describe_request)
        if not describe_response.volumes:
            return {"error": f"No volume found with ID: {volume_id}"}
            
        # 遍历所有volume
        volumes_data = []
        for volume in describe_response.volumes:
            volumes_data.append({
                "volume_id": volume.volume_id,
                "status": volume.status,
                "size": volume.size,
                # 添加其他需要的字段
            })
            
        return {
            "volumes": volumes_data,
            "count": len(volumes_data),
            "data": describe_response.to_str()
        }

    except Exception as e:
        logger.error(f"Error in describe_volume: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def describe_snapshot(
    snapshot_id: str,
    query: Optional[str] = None
) -> Dict:
    """Query information about a specific EBS snapshot.
    This tool retrieves details of an EBS snapshot including status, size, creation time etc.

    Args:
        snapshot_id: The ID of the EBS snapshot to query (e.g. "snap-12345678")
        query: Optional specific questions about the snapshot (status, size, creation time etc.)
    """
    logger.info(f"Received describe_snapshot request for snapshot: {snapshot_id}")

    try:
        describe_request = volcenginesdkstorageebs.DescribeSnapshotsRequest(
            snapshot_ids=[snapshot_id]
        )

        describe_response = ebs_cli.describe_snapshots(describe_request)

        snapshot = describe_response.snapshots[0]
        if not snapshot:
            return {"error": f"No snapshot found with ID: {snapshot_id}"}
                    
        # If query is provided, add additional processing logic here
        if query:
            # You can add NLP processing to answer specific questions
            pass
            
        return {
            "snapshot_id": snapshot_id,
            "data": describe_response.to_str()
        }

    except Exception as e:
        logger.error(f"Error in describe_snapshot: {str(e)}")
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Run the Storage EBS MCP Server")
    parser.add_argument("--transport", "-t", choices=["sse", "stdio"], default="stdio")
    parser.add_argument("--config", "-c", help="Path to config file")  # 新增config参数
    
    args = parser.parse_args()
    global config
    try:
        # 修改配置加载方式
        if args.config:
            config = load_config(args.config)
        else:
            config = load_config()
        # Initialize Storage EBS service
        global  ebs_cli
        logger.info(
            f"Initialized Storage EBS Base service"
        )

        # Initialize EBS service
        configuration = volcenginesdkcore.Configuration()
        configuration.host = config.endpoint
        configuration.region = config.region
        configuration.ak = config.access_key_id
        configuration.sk = config.access_key_secret
        configuration.zone = config.zone

        volcenginesdkcore.Configuration.set_default(configuration)
        ebs_cli = volcenginesdkstorageebs.STORAGEEBSApi()

        # Run the MCP server
        logger.info(
            f"Starting Storage EBS MCP Server with {args.transport} transport"
        )
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Storage EBS MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
