import numpy as np
import torch
from backend.agent import *
from backend.env import Env
from backend.data import *

def evaluate(environment, Defender, Attacker, nb_episodes=100, all_results=False):
    with torch.no_grad():
        total_return = []
        for ep in range(nb_episodes):
            current_return = evaluate_episode(
                environment, Defender, Attacker)
            total_return.append(current_return)
        total_return = np.array(total_return)
        avg_return = np.mean(total_return)
        std_return = np.std(total_return)
        return avg_return, std_return


def evaluate_episode(environment, Defender, Attacker):
    game_state = environment.reset()
    Attacker.reset()
    current_return = 0
    while not game_state.is_end():
        defender_obs, attacker_obs = game_state.obs()
        def_current_legal_action, att_current_legal_action = game_state.legal_action()

        defender_a = Defender.select_action(
            [defender_obs], [def_current_legal_action])
        attacker_a = Attacker.select_action()
        game_state = environment.simu_step(defender_a, attacker_a)
        def_reward, att_reward = game_state.reward()
        current_return += def_reward
    return current_return

def main(args=None):

    environment=Env('yishun')
    goals = EXITS
    theif = INIT_LOC[0]
    defenders = DEFENDER_INIT[0]
    limit=TIME_HORIZON
    Defender=AgentEvalYishun()
   
    Attacker = AllPathAttacker()
    for i in range(10):
        avg_return, std_return = evaluate(environment, Defender,
                                            Attacker, 500)
        print(avg_return)

    

if __name__ == "__main__":
    main()