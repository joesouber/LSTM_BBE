### ~ THREADED BRISTOL BETTING EXCHANGE ~ ###

# import sys, math, threading, time, queue, random, csv, config, pandas
# from copy import deepcopy


# from system_constants import *
# from betting_agents import *
# import numpy as np
# from race_simulator import Simulator
# from ex_ante_odds_generator import *
# from exchange import Exchange
# from message_protocols import *
# from session_stats import *
# from ODmodels import *


# class Session:

#     def __init__(self):
#         # Initialise exchanges
#         self.exchanges = {}
#         self.exchangeOrderQs = {}
#         self.exchangeThreads = []

#         # Initialise betting agents
#         self.bettingAgents = {}
#         self.bettingAgentQs = {}
#         self.bettingAgentThreads = []

#         self.OpinionDynamicsPlatform = None

#         # Needed attributes
#         self.startTime = None
#         self.numberOfTimesteps = None
#         self.lengthOfRace = None
#         self.event = threading.Event()
#         self.endOfInPlayBettingPeriod = None
#         self.winningCompetitor = None
#         self.distances = None

#         # Record keeping attributes
#         self.tape = []
#         self.priceRecord = {}
#         self.spreads = {}
#         self.opinion_hist = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_l = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_e = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_g = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_s = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.competitor_odds = {'time': [], 'odds': [], 'competitor': []}
#         self.competitor_distances = {'time': [], 'distance': [], 'competitor': []}

#         self.generateRaceData()
#         self.initialiseThreads()

#     def exchangeLogic(self, exchange, exchangeOrderQ):
#         """
#         Logic for thread running the exchange
#         """
#         #print("EXCHANGE " + str(exchange.id) + " INITIALISED...")
#         self.event.wait()
#         # While event is running, run logic for exchange

#         competitor_odds = {'time': [], 'odds': [], 'competitor': []}

#         while self.event.isSet():
#             timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
#             try: order = exchangeOrderQ.get(block=False)
#             except: continue

#             marketUpdates = {}
#             for i in range(NUM_OF_EXCHANGES):
#                 marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

#             if timeInEvent < self.endOfInPlayBettingPeriod:
#                 self.OpinionDynamicsPlatform.initiate_conversations(timeInEvent)
#                 self.OpinionDynamicsPlatform.update_opinions(timeInEvent, marketUpdates)

#             else:
#                 self.OpinionDynamicsPlatform.settle_opinions(self.winningCompetitor)



#             (transactions, markets) = exchange.processOrder(timeInEvent, order)

#             if transactions != None:
#                 for id, q in self.bettingAgentQs.items():
#                     update = exchangeUpdate(transactions, order, markets)
#                     q.put(update)


#     def agentLogic(self, agent, agentQ):
#         """
#         Logic for betting agent threads
#         """
#         #print("AGENT " + str(agent.id) + " INITIALISED...")
#         # Need to have pre-event betting period
#         self.event.wait()
#         # Whole event is running, run logic for betting agents
#         while self.event.isSet():
#             time.sleep(0.01)
#             timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
#             order = None
#             trade = None


#             while agentQ.empty() is False:
#                 qItem = agentQ.get(block = False)
#                 if qItem.protocolNum == EXCHANGE_UPDATE_MSG_NUM:
#                     for transaction in qItem.transactions:
#                         if transaction['backer'] == agent.id: agent.bookkeep(transaction, 'Backer', qItem.order, timeInEvent)
#                         if transaction['layer'] == agent.id: agent.bookkeep(transaction, 'Layer', qItem.order, timeInEvent)

#                 elif qItem.protocolNum == RACE_UPDATE_MSG_NUM:
#                     agent.observeRaceState(qItem.timestep, qItem.compDistances)
#                 else:
#                     print("INVALID MESSAGE")



#             marketUpdates = {}
#             for i in range(NUM_OF_EXCHANGES):
#                 marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

#             agent.respond(timeInEvent, marketUpdates, trade)
#             order = agent.getorder(timeInEvent, marketUpdates)


#             if agent.id == 0:
#                 for i in range(NUM_OF_COMPETITORS):
#                     self.competitor_odds['time'].append(timeInEvent)
#                     self.competitor_odds['competitor'].append(i)
#                     if marketUpdates[0][i]['backs']['n'] > 0:
#                         self.competitor_odds['odds'].append(marketUpdates[0][i]['backs']['best'])
#                     else:
#                         self.competitor_odds['odds'].append(marketUpdates[0][i]['backs']['worst'])

#                     self.competitor_distances['competitor'].append(i)
#                     self.competitor_distances['time'].append(timeInEvent)
#                     if len(agent.currentRaceState) == 0:
#                         self.competitor_distances['distance'].append(0)
#                     else:
#                         self.competitor_distances['distance'].append(agent.currentRaceState[i])


#             self.opinion_hist['id'].append(agent.id)
#             self.opinion_hist['time'].append(timeInEvent)
#             self.opinion_hist['opinion'].append(agent.opinion)
#             self.opinion_hist['competitor'].append(OPINION_COMPETITOR)

#             self.opinion_hist_e['id'].append(agent.id)
#             self.opinion_hist_e['time'].append(timeInEvent)
#             self.opinion_hist_e['opinion'].append(agent.event_opinion)
#             self.opinion_hist_e['competitor'].append(OPINION_COMPETITOR)

#             self.opinion_hist_l['id'].append(agent.id)
#             self.opinion_hist_l['time'].append(timeInEvent)
#             self.opinion_hist_l['opinion'].append(agent.local_opinion)
#             self.opinion_hist_l['competitor'].append(OPINION_COMPETITOR)

#             self.opinion_hist_g['id'].append(agent.id)
#             self.opinion_hist_g['time'].append(timeInEvent)
#             self.opinion_hist_g['opinion'].append(agent.global_opinion)
#             self.opinion_hist_g['competitor'].append(OPINION_COMPETITOR)

#             self.opinion_hist_s['id'].append(agent.id)
#             self.opinion_hist_s['time'].append(timeInEvent)
#             self.opinion_hist_s['opinion'].append(agent.strategy_opinion)
#             self.opinion_hist_s['competitor'].append(OPINION_COMPETITOR)

#             if order != None:

#                 if TBBE_VERBOSE:
#                     print(order)
#                 agent.numOfBets = agent.numOfBets + 1
#                 self.exchangeOrderQs[order.exchange].put(order)


#        # print("ENDING AGENT " + str(agent.id))
#         return 0

#     def populateMarket(self):
#         """
#         Populate market with betting agents as specified in config file
#         """
#         def initAgent(name, quantity, id):

#             uncertainty = 1.0

#             local_opinion = 1/ NUM_OF_COMPETITORS

#             #
#             # if name == 'Test': return Agent_Test(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Random': return Agent_Random(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Leader_Wins': return Agent_Leader_Wins(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Underdog': return Agent_Underdog(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Back_Favourite': return Agent_Back_Favourite(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Linex': return Agent_Linex(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Arbitrage': return Agent_Arbitrage(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Arbitrage2': return Agent_Arbitrage2(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)
#             # if name == 'Priveledged': return Agent_Priveledged(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod)

#             if name == 'Agent_Opinionated_Random': return Agent_Opinionated_Random(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP )
#             if name == 'Agent_Opinionated_Leader_Wins': return Agent_Opinionated_Leader_Wins(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP )
#             if name == 'Agent_Opinionated_Underdog': return Agent_Opinionated_Underdog(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == "Agent_Opinionated_Back_Favourite": return Agent_Opinionated_Back_Favourite(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'Agent_Opinionated_Linex': return Agent_Opinionated_Linex(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion,uncertainty, MIN_OP, MAX_OP)

#             if name == 'Agent_Opinionated_Priviledged': return Agent_Opinionated_Priviledged(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 1, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'XGBoostBettingAgent': return XGBoostBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion,uncertainty, MIN_OP, MAX_OP)
#             if name == 'LSTMBettingAgent': return LSTMBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion,uncertainty, MIN_OP, MAX_OP)

#         id = 0
#         for agent in config.agents:
#             type = agent[0]
#             for i in range(agent[1]):
#                 self.bettingAgents[id] = initAgent(agent[0], agent[1], id)
#                 id = id + 1

#     def initialiseExchanges(self):
#         """
#         Initialise exchanges, returns list of exchange objects
#         """
#         for i in range(NUM_OF_EXCHANGES):
#             self.exchanges[i] = Exchange(i, NUM_OF_COMPETITORS) # NUM_OF_COMPETITORS may be changed to list of competitor objects that are participating
#             self.exchangeOrderQs[i] = queue.Queue()

#     def initialiseBettingAgents(self):
#         """
#         Initialise betting agents
#         """
#         self.populateMarket()
#         self.OpinionDynamicsPlatform = OpinionDynamicsPlatform(list(self.bettingAgents.values()), MODEL_NAME)
#         print("initializating")
#         #print(list(self.bettingAgents.values()))
#         # Create threads for all betting agents that wait until event session
#         # has started
#         for id, agent in self.bettingAgents.items():
#             self.bettingAgentQs[id] = queue.Queue()
#             thread = threading.Thread(target = self.agentLogic, args = [agent, self.bettingAgentQs[id]])
#             self.bettingAgentThreads.append(thread)


#     def updateRaceQ(self, timestep):
#         """
#         Read in race data and update agent queues with competitor distances at timestep
#         """
#         with open(RACE_DATA_FILENAME, 'r') as file:
#             reader = csv.reader(file)
#             r = [row for index, row in enumerate(reader) if index == timestep]
#         time = r[0][0]
#         compDistances = {}
#         for c in range(NUM_OF_COMPETITORS):
#             compDistances[c] = float(r[0][c+1])

#         # Create update
#         update = raceUpdate(time, compDistances)

#         for id, q in self.bettingAgentQs.items():
#             q.put(update)

#     def preRaceBetPeriod(self):
#         print("Start of pre-race betting period, lasting " + str(PRE_RACE_BETTING_PERIOD_LENGTH))
#         time.sleep(PRE_RACE_BETTING_PERIOD_LENGTH / SESSION_SPEED_MULTIPLIER)
#         print("End of pre-race betting period")
#         # marketUpdates = {}
#         # for id, ex in exchanges.items():
#         #     timeInEvent = time.time() - startTime
#         #     print("Exchange " + str(id) + " markets: ")
#         #     print(exchanges[id].publishMarketState(timeInEvent))


#     def eventSession(self, simulationId):
#         """
#         Set up and management of race event
#         """

#         # Record start time
#         self.startTime = time.time()

#         # Start exchange threads
#         for id, exchange in self.exchanges.items():
#             thread = threading.Thread(target = self.exchangeLogic, args = [exchange, self.exchangeOrderQs[id]])
#             self.exchangeThreads.append(thread)

#         for thread in self.exchangeThreads:
#             thread.start()

#         # Start betting agent threads
#         for thread in self.bettingAgentThreads:
#             thread.start()

#         # Initialise event
#         self.event.set()

#         time.sleep(0.01)

#         # Pre-race betting period
#         self.preRaceBetPeriod()


#         # have loop which runs until competitor has won race
#         i = 0
#         while(i < self.numberOfTimesteps):
#             self.updateRaceQ(i+1)
#             i = i+1
#             if TBBE_VERBOSE: print(i)
#             print(i)
#             time.sleep(1 / SESSION_SPEED_MULTIPLIER)





#         # End event
#         self.event.clear()

#         # Close threads
#         for thread in self.exchangeThreads: thread.join()
#         for thread in self.bettingAgentThreads: thread.join()

#         print("Simulation complete")

#         print("Writing data....")
#         for id, ex in self.exchanges.items():
#             for orderbook in ex.compOrderbooks:
#                 for trade in orderbook.tape:
#                     #print(trade)
#                     self.tape.append(trade)

#         # Settle up all transactions over all exchanges
#         for id, ex in self.exchanges.items():
#             ex.settleUp(self.bettingAgents, self.winningCompetitor)

#         # for id, exchange in exchanges.items():
#         #     exchange.tapeDump('transactions.csv', 'a', 'keep')

#         for id, agent in self.bettingAgents.items():
#             print("Agent " + str(id) + "\'s final balance: " + str(agent.balance)+ " : "+str(agent.name))

#         createstats(self.bettingAgents, simulationId, self.tape, self.priceRecord, self.spreads, self.competitor_distances)

#     def initialiseThreads(self):
#         self.initialiseExchanges()
#         self.initialiseBettingAgents()

#     def generateRaceData(self):
#         # Create race event data
#         race = Simulator(NUM_OF_COMPETITORS)

#         compPool = deepcopy(race.competitors)
#         raceAttributes = deepcopy(race.race_attributes)


#         # create simulations for procurement of ex-ante odds for priveledged betters
#         createExAnteOdds(compPool, raceAttributes)

#         race.run("core")

#         self.numberOfTimesteps = race.numberOfTimesteps
#         self.lengthOfRace = race.race_attributes.length
#         self.winningCompetitor = race.winner
#         self.distances = race.raceData
#         self.endOfInPlayBettingPeriod = race.winningTimestep - IN_PLAY_CUT_OFF_PERIOD


#         createInPlayOdds(self.numberOfTimesteps)






# class BBE(Session):
#     def __init__(self):
#         self.session = None
#         return


#     # MAIN LOOP
#     # argFuncf is an optional function which sets up a new session (takes in a session)
#     def runSession(self, argFunc=None):
#         # Simulation attributes
#         currentSimulation = 0
#         ####################

#         # set things up
#         # have while loop for running multiple races
#         # within loop instantiate competitors into list
#         # run simulation and matching engine
#         while currentSimulation < NUM_OF_SIMS:
#             simulationId = "Simulation: " + str(currentSimulation)
#             # Start up thread for race on which all other threads will wait
#             self.session = Session()
#             if argFunc:
#                 argFunc(self.session)
#             self.session.eventSession(currentSimulation)

#             currentSimulation = currentSimulation + 1

#         # Opinion Dynamics results:

#         opinion_hist_df = pandas.DataFrame.from_dict(self.session.opinion_hist)
#         opinion_hist_df.to_csv('opinions.csv', index=False)

#         opinion_hist_df_l = pandas.DataFrame.from_dict(self.session.opinion_hist_l)
#         opinion_hist_df_l.to_csv('opinions_l.csv', index=False)

#         opinion_hist_df_g = pandas.DataFrame.from_dict(self.session.opinion_hist_g)
#         opinion_hist_df_g.to_csv('opinions_g.csv', index=False)

#         opinion_hist_df_e = pandas.DataFrame.from_dict(self.session.opinion_hist_e)
#         opinion_hist_df_e.to_csv('opinions_e.csv', index=False)

#         competitor_odds_df = pandas.DataFrame.from_dict(self.session.competitor_odds)
#         competitor_odds_df.to_csv('competitor_odds.csv', index=False)

#         competitor_distances_df = pandas.DataFrame.from_dict(self.session.competitor_distances)
#         competitor_distances_df.to_csv('competitor_distances.csv', index=False)
#         #print(competitor_distances_df)

#         opinion_hist_s_df = pandas.DataFrame.from_dict(self.session.opinion_hist_s)
#         opinion_hist_s_df.to_csv('opinion_hist_s.csv', index=False)


# if __name__ == "__main__":
#     import time

#     start = time.time()
#     # random.seed(26)
#     # np.random.seed(26)
#     print('Running')
#     bbe = BBE()
#     print('Running')
#     bbe.runSession()
#     end = time.time()
#     print('Time taken: ', end - start)


############################################################################################################
###########If i want alignment LSTM to work need to comment all above an uncomment all below :/#############
############################################################################################################


# import logging


# import sys, math, threading, time, queue, random, csv, config, pandas
# from copy import deepcopy

# from system_constants import *
# from betting_agents import *
# import numpy as np
# from race_simulator import Simulator
# from ex_ante_odds_generator import *
# from exchange import Exchange
# from message_protocols import *
# from session_stats import *
# from ODmodels import *


# class Session:
#     def __init__(self):
#         # Initialise exchanges
#         self.exchanges = {}
#         self.exchangeOrderQs = {}
#         self.exchangeThreads = []

#         # Initialise betting agents
#         self.bettingAgents = {}
#         self.bettingAgentQs = {}
#         self.bettingAgentThreads = []

#         self.OpinionDynamicsPlatform = None

#         # Needed attributes
#         self.startTime = None
#         self.numberOfTimesteps = None
#         self.lengthOfRace = None
#         self.event = threading.Event()
#         self.endOfInPlayBettingPeriod = None
#         self.winningCompetitor = None
#         self.distances = None

#         # Record keeping attributes
#         self.tape = []
#         self.priceRecord = {}
#         self.spreads = {}
#         self.opinion_hist = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_l = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_e = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_g = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.opinion_hist_s = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
#         self.competitor_odds = {'time': [], 'odds': [], 'competitor': []}
#         self.competitor_distances = {'time': [], 'distance': [], 'competitor': []}

#         self.generateRaceData()
#         self.initialiseThreads()

#     def exchangeLogic(self, exchange, exchangeOrderQ):
#         self.event.wait()
#         competitor_odds = {'time': [], 'odds': [], 'competitor': []}

#         while self.event.isSet():
#             timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
#             try:
#                 order = exchangeOrderQ.get(block=False)
#             except:
#                 continue

#             marketUpdates = {}
#             for i in range(NUM_OF_EXCHANGES):
#                 marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

#             if timeInEvent < self.endOfInPlayBettingPeriod:
#                 self.OpinionDynamicsPlatform.initiate_conversations(timeInEvent)
#                 self.OpinionDynamicsPlatform.update_opinions(timeInEvent, marketUpdates)
#             else:
#                 self.OpinionDynamicsPlatform.settle_opinions(self.winningCompetitor)

#             (transactions, markets) = exchange.processOrder(timeInEvent, order)

#             if transactions is not None:
#                 for id, q in self.bettingAgentQs.items():
#                     update = exchangeUpdate(transactions, order, markets)
#                     q.put(update)

#     def agentLogic(self, agent, agentQ):
#             """
#             Logic for betting agent threads
#             """
#             self.event.wait()
#             while self.event.isSet():
#                 time.sleep(0.01)
#                 timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
#                 order = None
#                 trade = None

#                 while agentQ.empty() is False:
#                     qItem = agentQ.get(block=False)
#                     if qItem.protocolNum == EXCHANGE_UPDATE_MSG_NUM:
#                         for transaction in qItem.transactions:
#                             if transaction['backer'] == agent.id: agent.bookkeep(transaction, 'Backer', qItem.order, timeInEvent)
#                             if transaction['layer'] == agent.id: agent.bookkeep(transaction, 'Layer', qItem.order, timeInEvent)
#                     elif qItem.protocolNum == RACE_UPDATE_MSG_NUM:
#                         agent.observeRaceState(qItem.timestep, qItem.compDistances)
#                     else:
#                         print("INVALID MESSAGE")

#                 marketUpdates = {}
#                 for i in range(NUM_OF_EXCHANGES):
#                     marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

#                 agent_distances_df = pd.DataFrame.from_dict(self.competitor_distances)

#                 # Check the agent type before calling the respond method
#                 if isinstance(agent, LSTMBettingAgent):
#                     agent.respond(timeInEvent, marketUpdates, trade, self.competitors, agent_distances_df)
#                 else:
#                     agent.respond(timeInEvent, marketUpdates, trade)

#                 order = agent.getorder(timeInEvent, marketUpdates)

#                 if order is not None:
#                     if TBBE_VERBOSE:
#                         print(order)
#                     agent.numOfBets += 1
#                     self.exchangeOrderQs[order.exchange].put(order)

#             return 0

#     def populateMarket(self):
#         def initAgent(name, quantity, id):
#             uncertainty = 1.0
#             local_opinion = 1 / NUM_OF_COMPETITORS

#             if name == 'Agent_Opinionated_Random':
#                 return Agent_Opinionated_Random(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'Agent_Opinionated_Leader_Wins':
#                 return Agent_Opinionated_Leader_Wins(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'Agent_Opinionated_Underdog':
#                 return Agent_Opinionated_Underdog(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == "Agent_Opinionated_Back_Favourite":
#                 return Agent_Opinionated_Back_Favourite(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'Agent_Opinionated_Linex':
#                 return Agent_Opinionated_Linex(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'Agent_Opinionated_Priviledged':
#                 return Agent_Opinionated_Priviledged(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 1, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'XGBoostBettingAgent':
#                 return XGBoostBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
#             if name == 'LSTMBettingAgent':
#                 return LSTMBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)

#         id = 0
#         for agent in config.agents:
#             type = agent[0]
#             for i in range(agent[1]):
#                 self.bettingAgents[id] = initAgent(agent[0], agent[1], id)
#                 id += 1

#     def initialiseExchanges(self):
#         for i in range(NUM_OF_EXCHANGES):
#             self.exchanges[i] = Exchange(i, NUM_OF_COMPETITORS)
#             self.exchangeOrderQs[i] = queue.Queue()

#     def initialiseBettingAgents(self):
#         self.populateMarket()
#         self.OpinionDynamicsPlatform = OpinionDynamicsPlatform(list(self.bettingAgents.values()), MODEL_NAME)
#         print("initializing")
#         for id, agent in self.bettingAgents.items():
#             self.bettingAgentQs[id] = queue.Queue()
#             thread = threading.Thread(target=self.agentLogic, args=[agent, self.bettingAgentQs[id]])
#             self.bettingAgentThreads.append(thread)

#     def updateRaceQ(self, timestep):
#         with open(RACE_DATA_FILENAME, 'r') as file:
#             reader = csv.reader(file)
#             r = [row for index, row in enumerate(reader) if index == timestep]
#         time = r[0][0]
#         compDistances = {c: float(r[0][c + 1]) for c in range(NUM_OF_COMPETITORS)}
#         update = raceUpdate(time, compDistances)

#         for id, q in self.bettingAgentQs.items():
#             q.put(update)

#     def preRaceBetPeriod(self):
#         print("Start of pre-race betting period, lasting " + str(PRE_RACE_BETTING_PERIOD_LENGTH))
#         time.sleep(PRE_RACE_BETTING_PERIOD_LENGTH / SESSION_SPEED_MULTIPLIER)
#         print("End of pre-race betting period")

#     def eventSession(self, simulationId):
#         self.startTime = time.time()

#         for id, exchange in self.exchanges.items():
#             thread = threading.Thread(target=self.exchangeLogic, args=[exchange, self.exchangeOrderQs[id]])
#             self.exchangeThreads.append(thread)

#         for thread in self.exchangeThreads:
#             thread.start()

#         for thread in self.bettingAgentThreads:
#             thread.start()

#         self.event.set()

#         time.sleep(0.01)

#         self.preRaceBetPeriod()

#         i = 0
#         while i < self.numberOfTimesteps:
#             self.updateRaceQ(i + 1)
#             i += 1
#             if TBBE_VERBOSE:
#                 print(i)
#             print(i)
#             time.sleep(1 / SESSION_SPEED_MULTIPLIER)

#         self.event.clear()

#         for thread in self.exchangeThreads:
#             thread.join()
#         for thread in self.bettingAgentThreads:
#             thread.join()

#         print("Simulation complete")
#         print("Writing data....")

#         for id, ex in self.exchanges.items():
#             for orderbook in ex.compOrderbooks:
#                 for trade in orderbook.tape:
#                     self.tape.append(trade)

#         for id, ex in self.exchanges.items():
#             ex.settleUp(self.bettingAgents, self.winningCompetitor)

#         for id, agent in self.bettingAgents.items():
#             print("Agent " + str(id) + "'s final balance: " + str(agent.balance) + " : " + str(agent.name))

#         createstats(self.bettingAgents, simulationId, self.tape, self.priceRecord, self.spreads, self.competitor_distances, self.competitors)

#     def initialiseThreads(self):
#         self.initialiseExchanges()
#         self.initialiseBettingAgents()

#     def generateRaceData(self):
#         race = Simulator(NUM_OF_COMPETITORS)
#         compPool = deepcopy(race.competitors)
#         raceAttributes = deepcopy(race.race_attributes)

#         self.competitors = compPool
#         self.race_attributes = raceAttributes.race_attributes_dict

#         for competitor in compPool:
#             competitor.alignment = competitor.calculateAlignment()

#         createExAnteOdds(compPool, raceAttributes)

#         race.run("core")

#         self.numberOfTimesteps = race.numberOfTimesteps
#         self.lengthOfRace = race.race_attributes.length
#         self.winningCompetitor = race.winner
#         self.distances = race.raceData
#         self.endOfInPlayBettingPeriod = race.winningTimestep - IN_PLAY_CUT_OFF_PERIOD

#         createInPlayOdds(self.numberOfTimesteps)


# class BBE(Session):
#     def __init__(self):
#         self.session = None
#         return

#     def runSession(self, argFunc=None):
#         currentSimulation = 0

#         while currentSimulation < NUM_OF_SIMS:
#             simulationId = "Simulation: " + str(currentSimulation)
#             self.session = Session()
#             if argFunc:
#                 argFunc(self.session)
#             self.session.eventSession(currentSimulation)

#             for agent_id, agent in self.session.bettingAgents.items():
#                 if isinstance(agent, LSTMBettingAgent):
#                     agent.session = self.session

#             agent_distances_df = pd.DataFrame.from_dict(self.session.competitor_distances)
#             getXGboostTrainData(self.session.tape, currentSimulation, self.session.bettingAgents, agent_distances_df, self.session.competitors)

#             currentSimulation += 1

#         opinion_hist_df = pandas.DataFrame.from_dict(self.session.opinion_hist)
#         opinion_hist_df.to_csv('opinions.csv', index=False)

#         opinion_hist_df_l = pandas.DataFrame.from_dict(self.session.opinion_hist_l)
#         opinion_hist_df_l.to_csv('opinions_l.csv', index=False)

#         opinion_hist_df_g = pandas.DataFrame.from_dict(self.session.opinion_hist_g)
#         opinion_hist_df_g.to_csv('opinions_g.csv', index=False)

#         opinion_hist_df_e = pandas.DataFrame.from_dict(self.session.opinion_hist_e)
#         opinion_hist_df_e.to_csv('opinions_e.csv', index=False)

#         competitor_odds_df = pandas.DataFrame.from_dict(self.session.competitor_odds)
#         competitor_odds_df.to_csv('competitor_odds.csv', index=False)

#         competitor_distances_df = pandas.DataFrame.from_dict(self.session.competitor_distances)
#         competitor_distances_df.to_csv('competitor_distances.csv', index=False)

#         opinion_hist_s_df = pandas.DataFrame.from_dict(self.session.opinion_hist_s)
#         opinion_hist_s_df.to_csv('opinion_hist_s.csv', index=False)



# if __name__ == "__main__":
#     import time

#     start = time.time()
#     print('Running')
#     bbe = BBE()
#     print('Running')
#     bbe.runSession()
#     end = time.time()
#     print('Time taken: ', end - start)

######################################################
########CODE ADDED FOR EXTENDED ANALYSIS FOR PAPER####
#######################################################




import logging


import sys, math, threading, time, queue, random, csv, config, pandas
from copy import deepcopy

from system_constants import *
from betting_agents import *
import numpy as np
from race_simulator import Simulator
from ex_ante_odds_generator import *
from exchange import Exchange
from message_protocols import *
from session_stats import *
from ODmodels import *


class Session:
    def __init__(self):
        # Initialise exchanges
        self.exchanges = {}
        self.exchangeOrderQs = {}
        self.exchangeThreads = []

        # Initialise betting agents
        self.bettingAgents = {}
        self.bettingAgentQs = {}
        self.bettingAgentThreads = []

        self.OpinionDynamicsPlatform = None

        # Needed attributes
        self.startTime = None
        self.numberOfTimesteps = None
        self.lengthOfRace = None
        self.event = threading.Event()
        self.endOfInPlayBettingPeriod = None
        self.winningCompetitor = None
        self.distances = None

        # Record keeping attributes
        self.tape = []
        self.priceRecord = {}
        self.spreads = {}
        self.opinion_hist = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
        self.opinion_hist_l = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
        self.opinion_hist_e = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
        self.opinion_hist_g = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
        self.opinion_hist_s = {'id': [], 'time': [], 'opinion': [], 'competitor': []}
        self.competitor_odds = {'time': [], 'odds': [], 'competitor': []}
        self.competitor_distances = {'time': [], 'distance': [], 'competitor': []}

        self.generateRaceData()
        self.initialiseThreads()

    def exchangeLogic(self, exchange, exchangeOrderQ):
        self.event.wait()
        competitor_odds = {'time': [], 'odds': [], 'competitor': []}

        while self.event.isSet():
            timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
            try:
                order = exchangeOrderQ.get(block=False)
            except:
                continue

            marketUpdates = {}
            for i in range(NUM_OF_EXCHANGES):
                marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

            if timeInEvent < self.endOfInPlayBettingPeriod:
                self.OpinionDynamicsPlatform.initiate_conversations(timeInEvent)
                self.OpinionDynamicsPlatform.update_opinions(timeInEvent, marketUpdates)
            else:
                self.OpinionDynamicsPlatform.settle_opinions(self.winningCompetitor)

            (transactions, markets) = exchange.processOrder(timeInEvent, order)

            if transactions is not None:
                for id, q in self.bettingAgentQs.items():
                    update = exchangeUpdate(transactions, order, markets)
                    q.put(update)

    def agentLogic(self, agent, agentQ):
            """
            Logic for betting agent threads
            """
            self.event.wait()
            while self.event.isSet():
                time.sleep(0.01)
                timeInEvent = (time.time() - self.startTime) / SESSION_SPEED_MULTIPLIER
                order = None
                trade = None

                while agentQ.empty() is False:
                    qItem = agentQ.get(block=False)
                    if qItem.protocolNum == EXCHANGE_UPDATE_MSG_NUM:
                        for transaction in qItem.transactions:
                            if transaction['backer'] == agent.id: agent.bookkeep(transaction, 'Backer', qItem.order, timeInEvent)
                            if transaction['layer'] == agent.id: agent.bookkeep(transaction, 'Layer', qItem.order, timeInEvent)
                    elif qItem.protocolNum == RACE_UPDATE_MSG_NUM:
                        agent.observeRaceState(qItem.timestep, qItem.compDistances)
                    else:
                        print("INVALID MESSAGE")

                marketUpdates = {}
                for i in range(NUM_OF_EXCHANGES):
                    marketUpdates[i] = self.exchanges[i].publishMarketState(timeInEvent)

                agent_distances_df = pd.DataFrame.from_dict(self.competitor_distances)

                # Check the agent type before calling the respond method
                if isinstance(agent, LSTMBettingAgent):
                    agent.respond(timeInEvent, marketUpdates, trade, self.competitors, agent_distances_df)
                else:
                    agent.respond(timeInEvent, marketUpdates, trade)

                order = agent.getorder(timeInEvent, marketUpdates)

                if order is not None:
                    if TBBE_VERBOSE:
                        print(order)
                    agent.numOfBets += 1
                    self.exchangeOrderQs[order.exchange].put(order)

            return 0

    def populateMarket(self):
        def initAgent(name, quantity, id):
            uncertainty = 1.0
            local_opinion = 1 / NUM_OF_COMPETITORS

            if name == 'Agent_Opinionated_Random':
                return Agent_Opinionated_Random(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'Agent_Opinionated_Leader_Wins':
                return Agent_Opinionated_Leader_Wins(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'Agent_Opinionated_Underdog':
                return Agent_Opinionated_Underdog(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == "Agent_Opinionated_Back_Favourite":
                return Agent_Opinionated_Back_Favourite(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'Agent_Opinionated_Linex':
                return Agent_Opinionated_Linex(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'Agent_Opinionated_Priviledged':
                return Agent_Opinionated_Priviledged(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 1, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'XGBoostBettingAgent':
                return XGBoostBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)
            if name == 'LSTMBettingAgent':
                return LSTMBettingAgent(id, name, self.lengthOfRace, self.endOfInPlayBettingPeriod, 0, local_opinion, uncertainty, MIN_OP, MAX_OP)

        id = 0
        for agent in config.agents:
            type = agent[0]
            for i in range(agent[1]):
                self.bettingAgents[id] = initAgent(agent[0], agent[1], id)
                id += 1

    def initialiseExchanges(self):
        for i in range(NUM_OF_EXCHANGES):
            self.exchanges[i] = Exchange(i, NUM_OF_COMPETITORS)
            self.exchangeOrderQs[i] = queue.Queue()

    def initialiseBettingAgents(self):
        self.populateMarket()
        self.OpinionDynamicsPlatform = OpinionDynamicsPlatform(list(self.bettingAgents.values()), MODEL_NAME)
        print("initializing")
        for id, agent in self.bettingAgents.items():
            self.bettingAgentQs[id] = queue.Queue()
            thread = threading.Thread(target=self.agentLogic, args=[agent, self.bettingAgentQs[id]])
            self.bettingAgentThreads.append(thread)

    def updateRaceQ(self, timestep):
        with open(RACE_DATA_FILENAME, 'r') as file:
            reader = csv.reader(file)
            r = [row for index, row in enumerate(reader) if index == timestep]
        time = r[0][0]
        compDistances = {c: float(r[0][c + 1]) for c in range(NUM_OF_COMPETITORS)}
        update = raceUpdate(time, compDistances)

        for id, q in self.bettingAgentQs.items():
            q.put(update)

    def preRaceBetPeriod(self):
        print("Start of pre-race betting period, lasting " + str(PRE_RACE_BETTING_PERIOD_LENGTH))
        time.sleep(PRE_RACE_BETTING_PERIOD_LENGTH / SESSION_SPEED_MULTIPLIER)
        print("End of pre-race betting period")

    def eventSession(self, simulationId):
        self.startTime = time.time()

        for id, exchange in self.exchanges.items():
            thread = threading.Thread(target=self.exchangeLogic, args=[exchange, self.exchangeOrderQs[id]])
            self.exchangeThreads.append(thread)

        for thread in self.exchangeThreads:
            thread.start()

        for thread in self.bettingAgentThreads:
            thread.start()

        self.event.set()

        time.sleep(0.01)

        self.preRaceBetPeriod()

        i = 0
        while i < self.numberOfTimesteps:
            self.updateRaceQ(i + 1)
            i += 1
            if TBBE_VERBOSE:
                print(i)
            print(i)
            time.sleep(1 / SESSION_SPEED_MULTIPLIER)

        self.event.clear()

        for thread in self.exchangeThreads:
            thread.join()
        for thread in self.bettingAgentThreads:
            thread.join()

        print("Simulation complete")
        print("Writing data....")

        for id, ex in self.exchanges.items():
            for orderbook in ex.compOrderbooks:
                for trade in orderbook.tape:
                    self.tape.append(trade)

        for id, ex in self.exchanges.items():
            ex.settleUp(self.bettingAgents, self.winningCompetitor)

        for id, agent in self.bettingAgents.items():
            print("Agent " + str(id) + "'s final balance: " + str(agent.balance) + " : " + str(agent.name))

        createstats(self.bettingAgents, simulationId, self.tape, self.priceRecord, self.spreads, self.competitor_distances, self.competitors)

    def initialiseThreads(self):
        self.initialiseExchanges()
        self.initialiseBettingAgents()

    def generateRaceData(self):
        race = Simulator(NUM_OF_COMPETITORS)
        compPool = deepcopy(race.competitors)
        raceAttributes = deepcopy(race.race_attributes)

        self.competitors = compPool
        self.race_attributes = raceAttributes.race_attributes_dict

        for competitor in compPool:
            competitor.alignment = competitor.calculateAlignment()

        createExAnteOdds(compPool, raceAttributes)

        race.run("core")

        self.numberOfTimesteps = race.numberOfTimesteps
        self.lengthOfRace = race.race_attributes.length
        self.winningCompetitor = race.winner
        self.distances = race.raceData
        self.endOfInPlayBettingPeriod = race.winningTimestep - IN_PLAY_CUT_OFF_PERIOD

        createInPlayOdds(self.numberOfTimesteps)


class BBE(Session):
    def runSession(self, argFunc=None):
        currentSimulation = 0

        while currentSimulation < NUM_OF_SIMS:
            simulationId = "Simulation: " + str(currentSimulation)
            self.session = Session()
            if argFunc:
                argFunc(self.session)
            self.session.eventSession(currentSimulation)

            for agent_id, agent in self.session.bettingAgents.items():
                if isinstance(agent, LSTMBettingAgent):
                    agent.session = self.session

            agent_distances_df = pd.DataFrame.from_dict(self.session.competitor_distances)
            getXGboostTrainData(self.session.tape, currentSimulation, self.session.bettingAgents, agent_distances_df, self.session.competitors)

            currentSimulation += 1

        opinion_hist_df = pandas.DataFrame.from_dict(self.session.opinion_hist)
        opinion_hist_df.to_csv('opinions.csv', index=False)

        opinion_hist_df_l = pandas.DataFrame.from_dict(self.session.opinion_hist_l)
        opinion_hist_df_l.to_csv('opinions_l.csv', index=False)

        opinion_hist_df_g = pandas.DataFrame.from_dict(self.session.opinion_hist_g)
        opinion_hist_df_g.to_csv('opinions_g.csv', index=False)

        opinion_hist_df_e = pandas.DataFrame.from_dict(self.session.opinion_hist_e)
        opinion_hist_df_e.to_csv('opinions_e.csv', index=False)

        competitor_odds_df = pandas.DataFrame.from_dict(self.session.competitor_odds)
        competitor_odds_df.to_csv('competitor_odds.csv', index=False)

        competitor_distances_df = pandas.DataFrame.from_dict(self.session.competitor_distances)
        competitor_distances_df.to_csv('competitor_distances.csv', index=False)

        opinion_hist_s_df = pandas.DataFrame.from_dict(self.session.opinion_hist_s)
        opinion_hist_s_df.to_csv('opinion_hist_s.csv', index=False)

        # Collect prediction scores
        xgboost_scores = []
        lstm_scores = []
        for agent in self.session.bettingAgents.values():
            if isinstance(agent, XGBoostBettingAgent):
                xgboost_scores.extend(agent.get_prediction_scores())
            elif isinstance(agent, LSTMBettingAgent):
                lstm_scores.extend(agent.get_prediction_scores())

        # Save prediction scores
        pd.DataFrame({'xgboost_scores': xgboost_scores}).to_csv('xgboost_scores.csv', index=False)
        pd.DataFrame({'lstm_scores': lstm_scores}).to_csv('lstm_scores.csv', index=False)

if __name__ == "__main__":
    import time

    start = time.time()
    print('Running')
    bbe = BBE()
    print('Running')
    bbe.runSession()
    end = time.time()
    print('Time taken: ', end - start)
   LSTM AGENT:   import pandas as pd
import joblib
import random
import operator
from keras.models import load_model
from message_protocols import Order
from system_constants import MIN_ODDS

class LSTMBettingAgent(BettingAgent):
    def __init__(self, id, name, lengthOfRace, endOfInPlayBettingPeriod, influenced_by_opinions,
                 local_opinion, uncertainty, lower_op_bound, upper_op_bound):
        super().__init__(id, name, lengthOfRace, endOfInPlayBettingPeriod, influenced_by_opinions,
                         local_opinion, uncertainty, lower_op_bound, upper_op_bound)
        self.lstm_loaded_model = load_model('/content/drive/MyDrive/greece_ablation/baseline/trained_lstm_model_baseline_greece.h5')
        self.scaler = joblib.load('/content/drive/MyDrive/greece_ablation/align_minmaxscaler_newgreece.pkl')
        self.bettingInterval = 1
        self.bettingTime = 0 #random.randint(5, 15)
        self.name = 'LSTMBettingAgent'
        self.bets_placed = 0  # Initialize a counter for bets placed
        self.prediction_scores = []

    def getorder(self, time, markets):
        order = None
        if len(self.orders) > 0:
            order = self.orders.pop()
        return order

    def make_decision(self, time, stake, distance, rank, odds, alignment):
        try:
            # Prepare features with all expected columns
            df = pd.DataFrame({
                'competitorID': [self.id],  # dummy value
                'time': [time],
                'exchange': [0],  # dummy value
                'odds': [odds],
                'agentID': [self.id],  # dummy value
                'stake': [stake],
                'distance': [distance],
                'rank': [rank],
                'balance': [self.balance],  # dummy value
                'decision': [0],  # dummy value
                'alignment': [alignment]
            })

            # Scale the input data
            scaled_data = self.scaler.transform(df)

            # Select only the relevant features for the LSTM model
            scaled_data = scaled_data[:, [df.columns.get_loc('time'),
                                          df.columns.get_loc('stake'),
                                          df.columns.get_loc('distance'),
                                          df.columns.get_loc('rank'),
                                          df.columns.get_loc('odds'),
                                          df.columns.get_loc('alignment')]]  # Include 'odds' and 'alignment'

            # Reshape for LSTM model input
            X_scaled = scaled_data.reshape((scaled_data.shape[0], 1, scaled_data.shape[1]))

            # Make a prediction using the LSTM model
            prediction = self.lstm_loaded_model.predict(X_scaled)[0][0]
            self.prediction_scores.append(prediction)
            decision = 1 if prediction > 0.5 else 0

            return decision
        except Exception as e:
            raise e

    def get_prediction_scores(self):
        return self.prediction_scores


    def respond(self, time, markets, trade, competitors, agent_distances):
        try:
            if self.bettingPeriod == False:
                return None
            order = None
            if self.raceStarted == False:
                return order

            if self.bettingTime <= self.raceTimestep and self.raceTimestep % self.bettingInterval == 0:
                sortedComps = sorted((self.currentRaceState.items()), key=operator.itemgetter(1))

                for rank, (competitor_id, distance) in enumerate(sortedComps):
                    # Extract distance and rank using the similar logic as getXGboostTrainData
                    epsilon = 1e-1
                    mask = (agent_distances['competitor'] == competitor_id) & (abs(agent_distances['time'] - time) < epsilon)
                    filtered_df = agent_distances[mask]
                    distance = filtered_df['distance'].values[0] if len(filtered_df) > 0 else 0
                    rank = filtered_df['rank'].values[0] if len(filtered_df) > 0 else 0

                    # Retrieve the alignment score for the current competitor
                    competitor = next(comp for comp in competitors if comp.id == competitor_id)
                    alignment = competitor.alignment

                    # Fetching odds from the market state
                    odds = markets[self.exchange][competitor_id]['backs']['best'] if markets[self.exchange][competitor_id]['backs']['n'] > 0 else markets[self.exchange][competitor_id]['backs']['worst']

                    decision = self.make_decision(time, 15, distance, rank + 1, odds, alignment)
                    if decision == 1:  # Decision = back
                        if markets[self.exchange][competitor_id]['backs']['n'] > 0:
                            quoteodds = max(MIN_ODDS, markets[self.exchange][competitor_id]['backs']['best'] - 0.1)
                        else:
                            quoteodds = markets[self.exchange][competitor_id]['backs']['worst']

                        order = Order(self.exchange, self.id, competitor_id, 'Back', quoteodds,
                                      random.randint(self.stakeLower, self.stakeHigher),
                                      markets[self.exchange][competitor_id]['QID'], time)

                        if order.direction == 'Back':
                            liability = self.amountFromOrders + order.stake
                            if liability > self.balance:
                                continue
                            else:
                                self.orders.append(order)
                                self.amountFromOrders = liability
                                self.bets_placed += 1

                    elif decision == 0:  # Decision = lay
                        if markets[self.exchange][competitor_id]['lays']['n'] > 0:
                            quoteodds = markets[self.exchange][competitor_id]['lays']['best'] + 0.1
                        else:
                            quoteodds = markets[self.exchange][competitor_id]['lays']['worst']

                        order = Order(self.exchange, self.id, competitor_id, 'Lay', quoteodds,
                                      random.randint(self.stakeLower, self.stakeHigher),
                                      markets[self.exchange][competitor_id]['QID'], time)

                        if order.direction == 'Lay':
                            liability = self.amountFromOrders + ((order.stake * order.odds) - order.stake)
                            if liability > self.balance:
                                continue
                            else:
                                self.orders.append(order)
                                self.amountFromOrders = liability
                                self.bets_placed += 1

        except Exception as e:
            raise e

