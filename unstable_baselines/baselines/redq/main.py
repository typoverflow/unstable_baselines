import os
import sys
# sys.path.append(os.path.join(os.getcwd(), './'))
# sys.path.append(os.path.join(os.getcwd(), '../..'))
import gym
import click
from unstable_baselines.common.logger import Logger
from unstable_baselines.baselines.redq.trainer import REDQTrainer
from unstable_baselines.baselines.redq.agent import REDQAgent
from unstable_baselines.common.env_wrapper import get_env, ScaleRewardWrapper
from unstable_baselines.common.util import set_device_and_logger, load_config, set_global_seed
from unstable_baselines.common.buffer import ReplayBuffer
from unstable_baselines.common import util

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument("config-path",type=str)
@click.option("--log-dir", default="logs/redq")
@click.option("--gpu", type=int, default=-1)
@click.option("--print-log", type=bool, default=True)
@click.option("--seed", type=int, default=35)
@click.option("--info", type=str, default="")
@click.option("--load_dir", type=str, default="")
@click.argument('args', nargs=-1)
def main(config_path, log_dir, gpu, print_log, seed, info, load_dir, args):
    #todo: add load and update parameters function
    args = load_config(config_path, args)

    #set global seed
    set_global_seed(seed)

    #initialize logger
    env_name = args['env_name']
    logger = Logger(log_dir, prefix = env_name+"-"+info, print_to_terminal=print_log)
    logger.log_str("logging to {}".format(logger.log_path))

    #set device and logger
    set_device_and_logger(gpu, logger)
    
    #save parameters
    logger.log_str_object("parameters", log_dict = args)

    #initialize environment
    env = get_env(env_name)
    env = ScaleRewardWrapper(env, **args['env'])
    eval_env = get_env(env_name)
    eval_env = ScaleRewardWrapper(eval_env, **args['env'])
    state_space = env.observation_space
    action_space = env.action_space

    #initialize buffer
    buffer = ReplayBuffer(state_space, action_space, **args['buffer'])

    #initialize agent
    logger.log_str("Initializing Agent")
    agent = REDQAgent(state_space, action_space, **args['agent'])

    #initialize trainer
    logger.log_str("Initializing Trainer")
    trainer  = REDQTrainer(
        agent,
        env,
        eval_env, 
        buffer,
        logger,
        load_dir=load_dir,
        **args['trainer']
    )
    
    logger.log_str("Started training")
    trainer.train()


if __name__ == "__main__":
    main()