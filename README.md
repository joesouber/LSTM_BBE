# LSTM_BBE

### This is code for An LSTM-Agent-Based model for In-Play Betting on a Sports Betting Exchange dissertation 

It is the extended version from A XGBoost-Agent Based model (https://github.com/ChawinT/XGBoost_TBBE). 

This version integrated an agent called LSTMBettingAgent to the original 'betting_agents.py' file in the Application folder. This agent uses the models trained from (https://github.com/joesouber/DeepLearningBBE_modeltraining/tree/main) to make the prediction. Moreover, this version also adapted a function called 'getXGboostTrainData' to 'session_stats.py' file to collects/gather data for LSTM model training. 

"createcores" and "launch8cores" are files that can be adjusted for your needs. They implement a parallel processing procedure accross avaliable CPU cores.

Basic steps for running the BBE (Bristol Betting Exchange): 
1. In config.py -> Initialize the agents list. Below is the example of agents list:
   agents = [('Agent_Opinionated_Random', 10), ('Agent_Opinionated_Leader_Wins', 10),
          ('Agent_Opinionated_Underdog', 10),('Agent_Opinionated_Back_Favourite',10),
          ('Agent_Opinionated_Linex', 10), ('Agent_Opinionated_Priviledged', 5),
          ('XGBoostBettingAgent', 5), ('LSTMBettingAgent', 5)]

   This will be the agent configuration that system uses when running the simulation. 

2. In systems_constant.py defines parameters/settings of the simulations. Example of parameters  systems_constant.py:

   -> General
  #NUM_OF_SIMS = 1
  NUM_OF_SIMS = 1
  NUM_OF_COMPETITORS = 5
  NUM_OF_EXCHANGES = 1
  PRE_RACE_BETTING_PERIOD_LENGTH = 0
  IN_PLAY_CUT_OFF_PERIOD = 0
  SESSION_SPEED_MULTIPLIER = 1

  -> Exchange Attributes
  MIN_ODDS = 1.1
  MAX_ODDS = 20.00

  -> Event Attributes
  RACE_LENGTH = 500
  MIN_RACE_LENGTH = 400
  MAX_RACE_LENGTH = 4000


3. "RUN" the session -> run TBBE.py file. 

4. After the session finished, results will be available in data folder. Many result files will be generated. Please look at session_stats.py file for how each file is generated.
5. useful files for model training include the "getXGBOOstTrainingData_{}.csv". For model testing and evaluation, "200_new_final_balance_{i}.csv", "xgboost_scores.csv", and "lstm_scores.csv" are useful.



### This github doens't contain data files due to a large files size. 
