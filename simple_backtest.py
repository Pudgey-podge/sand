from decimal import Decimal
from typing import Any, List, Optional
from dojo.config.config import load_network_cfg

from dojo.actions.uniswapV3 import UniswapV3Trade
from dojo.agents import BaseAgent, UniswapV3Agent
from dojo.environments.uniswapV3 import UniswapV3Observation
from dojo.policies import BasePolicy



class MyPolicy(BasePolicy):  # type: ignore
    """A policy that buys wrapped etherium."""

    def __init__(self, agent: BaseAgent):
        """Initialize the policy.

        :param agent: The agent which is using this policy.
        :param action: The action to execute.
        """
        super().__init__(agent)
        # rate of dumping

    def predict(self, obs):

        # print(self.agent.erc20_portfolio()["WETH"], "self.agent.erc20_portfolio()['WETH']")

        return []



class UniswapV3PoolWealthAgent(UniswapV3Agent):
    """This agent implements a pool wealth reward function for a single UniswapV3 pool.

    The agent should not be given any tokens that are not in the UniswapV3Env pool.
    """

    def __init__(
        self, initial_portfolio: dict[str, Decimal], name: Optional[str] = None
    ):
        """Initialize the agent."""
        super().__init__(name=name, initial_portfolio=initial_portfolio)

    def reward(self, obs: UniswapV3Observation) -> float:  # type: ignore
        """The agent wealth in units of asset y according to the UniswapV3 pool."""
        # define your PnL here, I'm happy to supply my own if asked.

        return Decimal(0)




import argparse
import logging
import time

from decimal import Decimal
from typing import Any, Optional



from dojo.common.constants import Chain
from dojo.environments import UniswapV3Env
from dojo.runners import backtest_run

import logging
import dojo.config.logging_config

dojo.config.logging_config.set_normal_logging_config(dojo_log_level=logging.DEBUG)


pool = "USDC/WETH-0.05"
print(pool)
chain = Chain.ETHEREUM

def get_start_block(pool: str, chain: Chain) -> int:
    cfg = load_network_cfg()
    return cfg.deployments[chain]["UniswapV3"][pool]["start_block"]

print(get_start_block(pool, chain))

# SNIPPET 1 START

pools = [pool]
start_block = get_start_block(pool, chain)
end_block = start_block + 500

# Agents
# , "xDAI": Decimal(1000000)
agent1 = UniswapV3PoolWealthAgent(
    initial_portfolio={
        "USDC": Decimal(50_000),
        "WETH": Decimal(25),
        "ETH": Decimal(10),
    },
    name="gary_the_agent",
)

env = UniswapV3Env(
    chain=Chain.ETHEREUM,
    block_range=(start_block, end_block),
    agents=[agent1],
    pools=pools,
    backend_type='forked',
    market_impact="replay",
)

# Policies
policy = MyPolicy(agent=agent1)

backtest_run(
    env,
    [policy],
    dashboard_server_port=1066,
    auto_close=True,
    simulation_status_bar=True,
)