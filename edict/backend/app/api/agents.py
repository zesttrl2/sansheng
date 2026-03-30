"""Agents API — Agent 配置和状态查询。"""

import json
import logging
from pathlib import Path

from fastapi import APIRouter

log = logging.getLogger("edict.api.agents")
router = APIRouter()

# Agent 元信息（对应 agents/ 目录下的 SOUL.md）
AGENT_META = {
    "zaochao": {"name": "早朝（朝会主持）", "role": "朝会召集与议程管理", "icon": "🏛️"},
    "zongjian": {"name": "AIGC项目总监", "role": "皇上代理与规划决策", "icon": "👑"},
    "zhijian": {"name": "AIGC质检", "role": "审议把关", "icon": "🔍"},
    "jiexi": {"name": "AIGC解析剧本", "role": "执行调度", "icon": "📜"},
    "fenjing": {"name": "AIGC分镜导演", "role": "文档与对外沟通", "icon": "📋"},
    "juesesheji": {"name": "AIGC角色场景道具设计师", "role": "数据分析与资源管理", "icon": "💰"},
    "juben": {"name": "AIGC剧本生成", "role": "基础设施与部署运维", "icon": "🔧"},
    "tuxiang": {"name": "AIGC图像生成", "role": "质量保障与合规审计", "icon": "⚖️"},
    "shipin": {"name": "AIGC视频生成", "role": "工程实现与功能开发", "icon": "🛡️"},
    "hr": {"name": "AIGC人事", "role": "人事管理与团队建设", "icon": "👤"},
}


@router.get("")
async def list_agents():
    """列出所有可用 Agent。"""
    agents = []
    for agent_id, meta in AGENT_META.items():
        agents.append({
            "id": agent_id,
            **meta,
        })
    return {"agents": agents}


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """获取 Agent 详情。"""
    meta = AGENT_META.get(agent_id)
    if not meta:
        return {"error": f"Agent '{agent_id}' not found"}, 404

    # 尝试读取 SOUL.md
    soul_path = Path(__file__).parents[4] / "agents" / agent_id / "SOUL.md"
    soul_content = ""
    if soul_path.exists():
        soul_content = soul_path.read_text(encoding="utf-8")[:2000]

    return {
        "id": agent_id,
        **meta,
        "soul_preview": soul_content,
    }


@router.get("/{agent_id}/config")
async def get_agent_config(agent_id: str):
    """获取 Agent 运行时配置。"""
    config_path = Path(__file__).parents[4] / "data" / "agent_config.json"
    if not config_path.exists():
        return {"agent_id": agent_id, "config": {}}

    try:
        configs = json.loads(config_path.read_text(encoding="utf-8"))
        agent_config = configs.get(agent_id, {})
        return {"agent_id": agent_id, "config": agent_config}
    except (json.JSONDecodeError, IOError):
        return {"agent_id": agent_id, "config": {}}
