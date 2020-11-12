'''
Polling places

Evelyn Dang, Corry Ke

Main file for polling place simulation
'''

import sys
import random
import queue
import click
import util



class Voter:
    def __init__(self, arrival_time, voting_duration):
        '''
        Constructor for the Voter class

        Inputs:
        arrival_time: (float) time that voter arrives
        voting_duration: (int) number of minutes taken to vote
        '''

        self.arrival_time = arrival_time
        self.voting_duration = voting_duration
        self.start_time = None
        self.departure_time = None

class Precinct(object):
    def __init__(self, name, hours_open, max_num_voters,
                 num_booths, arrival_rate, voting_duration_rate):
        '''
        Constructor for the Precinct class

        Input:
            name: (str) Name of the precinct
            hours_open: (int) Hours the precinct will remain open
            max_num_voters: (int) Number of voters in the precinct
            num_booths: (int) Number of voting booths in the precinct
            arrival_rate: (float) Rate at which voters arrive
            voting_duration_rate: (float) Lambda for voting duration
        '''

        self.name = name
        self.hours_open = hours_open
        self.max_num_voters = max_num_voters
        self.num_booths = num_booths
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate

    def next_voter(self, time, percent_straight_ticket):
        '''
        Returns the next voter in a precinct, with the start time 
            and departure time set as None

        Inputs:
        time: (float) the time where the current voter has finished
        percent_straight_ticket: (float) percentage of voters voting a straight ticket

        Output: 
        Voter class object, the next voter in the precinct 
        '''

        gap, voting_duration = util.gen_voter_parameters(self.arrival_rate, 
                                                        self.voting_duration_rate, 
                                                        percent_straight_ticket, 
                                                        straight_ticket_duration=2)
        next_voter = Voter(time + gap, voting_duration)

        return next_voter


    def simulate(self, percent_straight_ticket, straight_ticket_duration, seed):
        '''
        Simulate a day of voting

        Input:
            percent_straight_ticket: (float) Percentage of straight-ticket
              voters as a decimal between 0 and 1 (inclusive)
            straight_ticket_duration: (float) Voting duration for
              straight-ticket voters
            seed: (int) Random seed to use in the simulation

        Output:
            List of voters who voted in the precinct
        '''

        random.seed(seed)
        voters = []
        booths = VotingBooths(self.num_booths)
        minutes_open = self.hours_open * 60

        t = 0

        for i in range(self.max_num_voters):

            gap, voting_duration = util.gen_voter_parameters(self.arrival_rate, 
                                            self.voting_duration_rate, percent_straight_ticket, straight_ticket_duration=2)   
            
            next_arrival = t + gap
            t = next_arrival

            if t >= minutes_open:
                break
           
            elif t == next_arrival:
                voter = Voter(t, voting_duration)
                if not booths.is_full(): 
                    booths.add_voter(voter, t, voting_duration)
                else: 
                    latest_departure = booths.remove_voter()
                    if latest_departure > t:
                        booths.add_voter(voter, latest_departure, voting_duration)
                    else:
                        booths.add_voter(voter, t, voting_duration)
                voters.append(voter)
         
        return voters


class VotingBooths(object):
    '''
    Voting booths in a precinct
    '''

    def __init__(self, num_booths):
        '''
        Constructor

        Input:
            num_booths: (int) the number of booths in a precinct
        '''

        self.__pq = queue.PriorityQueue(maxsize = num_booths)


    def add_voter(self, voter, start_time, voting_duration):
        '''
        Adds a voter to the booth
        
        Input:
            voter: (Voter) the new voter
            start_time: (float) time our new voter started voting
            voting_duration: (float) time it took the new voter to vote
        
        Output: None
        '''

        voter.start_time = start_time
        voter.departure_time = start_time + voting_duration
        self.__pq.put(voter.departure_time, block = False) 
    

    def remove_voter(self):
        '''
        Removes a voter from the voting booth
        
        Input: None
        
        Output: (float) time of departure
        '''

        departure_time = self.__pq.get(block = False)

        return departure_time
    

    def is_empty(self):
        '''
        Check if voting booths are empty
        
        Input: None

        Output: (bool)
        '''
        
        return self.__pq.empty()


    def is_full(self):
        '''
        Check if voting booths are full

        Input: None

        Output: (bool)
        '''

        return self.__pq.full()


def find_avg_wait_time(precinct, percent_straight_ticket, ntrials, initial_seed = 0):
    '''
    Simulates a precinct multiple times with a given percentage of
    straight-ticket voters. For each simulation, computes the average
    waiting time of the voters, and returns the median of those average
    waiting times.

    Input:
        precinct: (dictionary) A precinct dictionary
        percent_straight_ticket: (float) Percentage straight-ticket voters
        ntrials: (int) The number of trials to run
        initial_seed: (int) Initial seed for random number generator

    Output:
        The median of the average waiting times returned by simulating
        the precinct 'ntrials' times.
    '''

    name = precinct['name']
    hours_open = precinct['hours_open']
    max_num_voters = precinct['num_voters']
    arrival_rate = precinct['arrival_rate']
    num_booths = precinct['num_booths']
    voting_duration = precinct['voting_duration_rate']
    straight_duration = precinct['straight_ticket_duration']
    p = Precinct(name, hours_open, max_num_voters, 
                num_booths, arrival_rate, voting_duration)

    seed = initial_seed
    avg_times = []

    for i in range(ntrials):
        sim = p.simulate(percent_straight_ticket, straight_duration, seed)
        total_wait = 0
        for voter in sim:
            total_wait += voter.start_time - voter.arrival_time
        avg_wait = total_wait / max_num_voters
        avg_times.append(avg_wait)
        seed += 1
    
    sorted_times = sorted(avg_times)
        
    return sorted_times[ntrials // 2]


def find_percent_split_ticket(precinct, target_wait_time, ntrials, seed=0):
    '''
    Finds the percentage of split-ticket voters needed to bound
    the (average) waiting time.

    Input:
        precinct: (dictionary) A precinct dictionary
        target_wait_time: (float) The minimum waiting time
        ntrials: (int) The number of trials to run when computing
                 the average waiting time
        seed: (int) A random seed

    Output:
        A tuple (percent_split_ticket, waiting_time) where:
        - percent_split_ticket: (float) The percentage of split-ticket
                                voters that ensures the average waiting time
                                is above target_waiting_time
        - waiting_time: (float) The actual average waiting time with that
                        percentage of split-ticket voters

        If the target waiting time is infeasible, returns (0, None)
    '''

    lst = list(range(11))
    percent_split_ticket = [round(i * 0.1, 1) for i in lst]

    for percent in percent_split_ticket:
        percent_split = percent
        avg_wait_time = find_avg_wait_time(precinct, 1 - percent, ntrials, seed)
        if avg_wait_time > target_wait_time:
            break
        elif percent == 1 and avg_wait_time < target_wait_time:
            avg_wait_time = None
         
    return (percent_split, avg_wait_time)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals
# pylint: disable-msg= missing-docstring, too-many-branches
# pylint: disable-msg= line-too-long
@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, target_wait_time, print_voters):
    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = {}
        for p in precincts:
            precinct = Precinct(p["name"],
                                p["hours_open"],
                                p["num_voters"],
                                p["num_booths"],
                                p["arrival_rate"],
                                p["voting_duration_rate"])
            voters[p["name"]] = precinct.simulate(p["percent_straight_ticket"], p["straight_ticket_duration"], seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    sys.exit(-1)
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        percent, avg_wt = find_percent_split_ticket(precinct, target_wait_time, 20, seed)

        if percent == 0:
            msg = "Waiting times are always below {:.2f}"
            msg += " in precinct '{}'"
            print(msg.format(target_wait_time, precinct["name"]))
        else:
            msg = "Precinct '{}' exceeds average waiting time"
            msg += " of {:.2f} with {} percent split-ticket voters"
            print(msg.format(precinct["name"], avg_wt, percent*100))


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
