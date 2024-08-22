# import sys, math, threading, time, queue, random, csv, config, random, operator
# from message_protocols import Order
# from system_constants import *
# import pandas as pd 



# def recordPrices(timestep, exchanges, record):
#     for id, ex in exchanges.items():
#         compData = {}
#         for orderbook in ex.compOrderbooks:
#             ob = orderbook.backs.bestOdds
#             ol = orderbook.lays.bestOdds

#             if(ob == None and ol == None):
#                 compData[orderbook.competitorId] = MAX_ODDS
#             elif(ob == None):
#                 compData[orderbook.competitorId] = ol
#             elif(ol == None):
#                 compData[orderbook.competitorId] = ob
#             else:
#                 print(ob)
#                 print(ol)
#                 print(orderbook.backs.market)
#                 print("BANG")
#                 print(orderbook.lays.market)
#                 qtyB = orderbook.backs.market[ob][0]
#                 qtyL = orderbook.lays.market[ol][0]

#                 microprice = ((ob * qtyL) + (ol * qtyB)) / (qtyB + qtyL)

#                 compData[orderbook.competitorId] = microprice

#         record[timestep] = compData

# def recordSpread(timestep, exchanges, record):
#     for id, ex in exchanges.items():
#         compData = {}
#         for orderbook in ex.compOrderbooks:
#             ob = orderbook.backs.bestOdds
#             ol = orderbook.lays.bestOdds



#             if(ob != None and ol != None):
#                 spread = abs((1/ob) - (1/ol))

#                 if spread != 0:
#                     compData[orderbook.competitorId] = spread

#         record[timestep] = compData

# def price_histories(priceHistory, simId):
#     history = []
#     for id, items in priceHistory.items():
#         history.append(items)

#     rows = [ [k] + [ (MAX_ODDS if (z == None) else z) for c, z in v.items() ] for k, v in priceHistory.items() ]

#     header = ["Time"]
#     for c in range(NUM_OF_COMPETITORS):
#         header.append(str(c))


#     print(rows)



#     fileName = "price_histories_" + str(simId) + ".csv"
#     with open(fileName, 'w', newline = '') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         writer.writerows(rows)

# def price_spread(spreadHistory, simId):

#     rows = [ [k] + [ (MAX_ODDS if (z == None) else z) for c, z in v.items() ] for k, v in spreadHistory.items() ]

#     header = ["Time"]
#     for c in range(NUM_OF_COMPETITORS):
#         header.append(str(c))

#     # print(priceHistory)
#     print(rows)

#     fileName = "price_spreads_" + str(simId) + ".csv"
#     with open(fileName, 'w', newline = '') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         writer.writerows(rows)


# def priv_bettor_odds(bettingAgents):
#     privBettors = []
#     for id, agent in bettingAgents.items():
#         if agent.name == 'Priveledged' or agent.name=='Agent_Opinionated_Priviledged': privBettors.append(agent)

#     oddsdata = {}
#     for b in privBettors:
#         oddsdata[b.id] = b.oddsData

#     header = ["Time"]
#     for c in range(NUM_OF_COMPETITORS):
#         header.append(str(c))

#     for b in privBettors:
#         fileName = "comp_odds_by_" + str(b.id) + ".csv"
#         with open(fileName, 'w', newline = '') as file:
#             writer = csv.writer(file)
#             writer.writerow(header)
#             writer.writerows(b.oddsData)


# def final_balances(bettingAgents, simId):
#     bettors = []
#     for id, agent in bettingAgents.items():
#         bettors.append(agent)

#     header = []
#     for i in range(len(bettors)):
#         header.append(str(i))

#     data = []
#     for i in range(len(bettors)):
#         data.append(bettors[i].balance)
    
#     fileName = "200_new_final_balance_" + str(simId) + ".csv"
#     with open(fileName, 'w', newline = '') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         writer.writerow(data)




# def transactions(trades, simId):
#     header = ["type", "time", "exchange", "competitor", "odds", "backer", "layer", "stake"]
#     tape = []
#     for val in trades:
#         temp = []
#         for i, v in val.items():
#             temp.append(v)
#         tape.append(temp)


#     fileName = "transactions_" + str(simId) + ".csv"
#     with open(fileName, 'w', newline = '') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         writer.writerows(tape)



# def getBalance(bettingAgents):
#     """
#     Retrieve the balance for each betting agent.
#     """
#     bettors = [agent for _, agent in bettingAgents.items()]

#     balances = {}
#     for i, bettor in enumerate(bettors):
#         balances[i] = bettor.balance

#     return balances

# def getXGboostTrainData(trades, simId, bettingAgents, agentDistances):
#     """
#     Process and format trade data for XGBoost training.
#     :trades: List of trade data.
#     :simId: Simulation ID.
#     :bettingAgents: Dictionary of betting agents.
#     :agentDistances: DataFrame containing distances for each competitor and time.
#     """
#     # Get the balances for each agent
#     balances = getBalance(bettingAgents)

#     # Compute the ranks for each competitor and time
#     agentDistances['rank'] = agentDistances.groupby('time')['distance'].rank(ascending=False, method='first').astype(int)

#     # Adjust the order of columns
#     new_header = ["type","competitorID", "time", "exchange", "odds",  "agentID", "stake", "distance", "rank", "balance", "decision"]

#     tape = [] # This will hold our final data rows
#     for val in trades:
#         competitor = val["competitor"]
#         time = val["time"]

#         # Define a tolerance level to match times approximately
#         tolerance = 1e-1
        
#         # Filter the distances dataframe for matching competitor and times
#         mask = (agentDistances['competitor'] == competitor) & (abs(agentDistances['time'] - time) < tolerance)
#         filtered_df = agentDistances[mask]
#         distance = filtered_df['distance'].values[0] if len(filtered_df) > 0 else 0 
#         rank = filtered_df['rank'].values[0] if len(filtered_df) > 0 else 0 

#         # Extract and format data for backer
#         backer_balance = balances[val["backer"]]
#         backer_row = [val["type"], val["competitor"], val["time"], val["exchange"], val["odds"], val["backer"], val["stake"], distance, rank, backer_balance, "backer"]
#         tape.append(backer_row)

#         # Extract and format data for layer
#         layer_balance = balances[val["layer"]]
#         layer_row = [val["type"], val["competitor"], val["time"], val["exchange"], val["odds"],  val["layer"], val["stake"], distance, rank, layer_balance, "layer"]
#         tape.append(layer_row)

#     # Write the final data rows to a CSV file
#     fileName = "getXGBOOstTrainingData_" + str(simId) + ".csv"
#     with open(fileName, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(new_header)
#         writer.writerows(tape)


# def createstats(bettingAgents, simId, trades, priceHistory, spreadHistory,AgentDistance):
#     priv_bettor_odds(bettingAgents)
#     final_balances(bettingAgents, simId)
#     price_histories(priceHistory, simId)
#     price_spread(spreadHistory, simId)
#     transactions(trades, simId)
#     getXGboostTrainData(trades, simId,bettingAgents,pd.DataFrame.from_dict(AgentDistance))







############################################################################################################
###########If i want alignment LSTM to work need to comment all above an uncomment all below :/ #############
############################################################################################################

import sys, math, threading, time, queue, random, csv, config, random, operator
from message_protocols import Order
from system_constants import *
import pandas as pd 



def recordPrices(timestep, exchanges, record):
    for id, ex in exchanges.items():
        compData = {}
        for orderbook in ex.compOrderbooks:
            ob = orderbook.backs.bestOdds
            ol = orderbook.lays.bestOdds

            if(ob == None and ol == None):
                compData[orderbook.competitorId] = MAX_ODDS
            elif(ob == None):
                compData[orderbook.competitorId] = ol
            elif(ol == None):
                compData[orderbook.competitorId] = ob
            else:
                print(ob)
                print(ol)
                print(orderbook.backs.market)
                print("BANG")
                print(orderbook.lays.market)
                qtyB = orderbook.backs.market[ob][0]
                qtyL = orderbook.lays.market[ol][0]

                microprice = ((ob * qtyL) + (ol * qtyB)) / (qtyB + qtyL)

                compData[orderbook.competitorId] = microprice

        record[timestep] = compData

def recordSpread(timestep, exchanges, record):
    for id, ex in exchanges.items():
        compData = {}
        for orderbook in ex.compOrderbooks:
            ob = orderbook.backs.bestOdds
            ol = orderbook.lays.bestOdds


            if(ob != None and ol != None):
                spread = abs((1/ob) - (1/ol))

                if spread != 0:
                    compData[orderbook.competitorId] = spread

        record[timestep] = compData

def price_histories(priceHistory, simId):
    history = []
    for id, items in priceHistory.items():
        history.append(items)

    rows = [ [k] + [ (MAX_ODDS if (z == None) else z) for c, z in v.items() ] for k, v in priceHistory.items() ]

    header = ["Time"]
    for c in range(NUM_OF_COMPETITORS):
        header.append(str(c))


    print(rows)



    fileName = "price_histories_" + str(simId) + ".csv"
    with open(fileName, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

def price_spread(spreadHistory, simId):

    rows = [ [k] + [ (MAX_ODDS if (z == None) else z) for c, z in v.items() ] for k, v in spreadHistory.items() ]

    header = ["Time"]
    for c in range(NUM_OF_COMPETITORS):
        header.append(str(c))


    print(rows)

    fileName = "price_spreads_" + str(simId) + ".csv"
    with open(fileName, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def priv_bettor_odds(bettingAgents):
    privBettors = []
    for id, agent in bettingAgents.items():
        if agent.name == 'Priveledged' or agent.name=='Agent_Opinionated_Priviledged': privBettors.append(agent)

    oddsdata = {}
    for b in privBettors:
        oddsdata[b.id] = b.oddsData

    header = ["Time"]
    for c in range(NUM_OF_COMPETITORS):
        header.append(str(c))

    for b in privBettors:
        fileName = "comp_odds_by_" + str(b.id) + ".csv"
        with open(fileName, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(b.oddsData)


def final_balances(bettingAgents, simId):
    bettors = []
    for id, agent in bettingAgents.items():
        bettors.append(agent)

    header = []
    for i in range(len(bettors)):
        header.append(str(i))

    data = []
    for i in range(len(bettors)):
        data.append(bettors[i].balance)
    
    fileName = "200_new_final_balance_" + str(simId) + ".csv"
    with open(fileName, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)




def transactions(trades, simId):
    header = ["type", "time", "exchange", "competitor", "odds", "backer", "layer", "stake"]
    tape = []
    for val in trades:
        temp = []
        for i, v in val.items():
            temp.append(v)
        tape.append(temp)


    fileName = "transactions_" + str(simId) + ".csv"
    with open(fileName, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tape)


def getBalance(bettingAgents):
    """
    Retrieve the balance for each betting agent.
    """
    bettors = [agent for _, agent in bettingAgents.items()]

    balances = {}
    for i, bettor in enumerate(bettors):
        balances[i] = bettor.balance

    return balances

# Modified getXGboostTrainData Function
def getXGboostTrainData(trades, simId, bettingAgents, agentDistances, competitors):
    # Get the current balance of all betting agents
    balances = getBalance(bettingAgents)

    # Compute the rank of each competitor for every time point
    # Ranking is based on the distance, with higher distances getting a better rank (lower number)
    agentDistances['rank'] = agentDistances.groupby('time')['distance'].rank(ascending=False, method='first').astype(int)
    print(agentDistances)  # Debugging output to verify the calculated ranks

    # Define the new header for the CSV file that will store the training data
    new_header = ["type", "time", "exchange", "competitor", "odds", "agentID", "decision", "stake", "balance", "distance", "rank", "alignment"]

    # Initialize an empty list to store the processed rows that will be written to the CSV file
    tape = []

    # Calculate the alignment score for each competitor
    for competitor in competitors:
        competitor.alignment = competitor.calculateAlignment()

    # Iterate through each trade in the list of trades
    for val in trades:
        competitor_id = val["competitor"]  # Get the competitor ID for the current trade
        time = val["time"]  # Get the time of the current trade

        # Use a small epsilon to account for floating-point precision when comparing times
        tolerance = 1e-1

        # Filter the agentDistances dataframe to find the entry corresponding to the current competitor and time
        mask = (agentDistances['competitor'] == competitor_id) & (abs(agentDistances['time'] - time) < tolerance)
        filtered_df = agentDistances[mask]

        # Extract the distance and rank for the current competitor at the given time
        distance = filtered_df['distance'].values[0] if len(filtered_df) > 0 else 0
        rank = filtered_df['rank'].values[0] if len(filtered_df) > 0 else 0

        # Retrieve the alignment score for the current competitor from the competitors list
        competitor = next(comp for comp in competitors if comp.id == competitor_id)
        alignment = competitor.alignment

        # Create a row for the backer with all relevant data, including balance, distance, rank, and alignment
        backer_balance = balances[val["backer"]]
        backer_row = [val["type"], val["time"], val["exchange"], val["competitor"], val["odds"], val["backer"], "backer", val["stake"], backer_balance, distance, rank, alignment]
        tape.append(backer_row)

        # Create a row for the layer with all relevant data, including balance, distance, rank, and alignment
        layer_balance = balances[val["layer"]]
        layer_row = [val["type"], val["time"], val["exchange"], val["competitor"], val["odds"], val["layer"], "layer", val["stake"], layer_balance, distance, rank, alignment]
        tape.append(layer_row)

    # Define the filename for the CSV file where the training data will be saved
    fileName = "getXGboostTrainingData_" + str(simId) + ".csv"

    # Open the CSV file for writing and write the header and all collected rows (tape)
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_header)  # Write the header row
        writer.writerows(tape)  # Write all the processed rows


# Modified createstats Function
def createstats(bettingAgents, simId, trades, priceHistory, spreadHistory, AgentDistance, competitors):
    final_balances(bettingAgents, simId)
    transactions(trades, simId)
    price_histories(priceHistory, simId)
    price_spread(spreadHistory, simId)
    priv_bettor_odds(bettingAgents)
    getXGboostTrainData(trades, simId, bettingAgents, pd.DataFrame.from_dict(AgentDistance), competitors)








