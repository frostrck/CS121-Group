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
        id: a voter identifier
        arrival_time: (int) time that voter arrives
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
        Returns the next voter in a precinct, with the start time and departure time set as None

        Inputs:
        time: int
        '''

        gap, voting_duration = util.gen_voter_parameters(arrival_rate, voting_duration_rate, percent_straight_ticket, straight_ticket_duration=2)
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
        voter_count = 0

        gap, voting_duration = util.gen_voter_parameters(self.arrival_rate, self.voting_duration_rate, percent_straight_ticket, straight_ticket_duration=2)
        
        next_arrival = gap
        next_service = next_arrival + voting_duration

        t = next_arrival

        while t <= minutes_open and voter_count < self.max_num_voters:
            if t == next_arrival:

                voter = Voter(arrival_time = t, voting_duration = voting_duration)
                if not booths.is_full(): 
                    voter.start_time = t
                    voter.departure_time = t + voting_duration
                    booths.add_voter(voter.departure_time)

                else: 
                    latest_departure = booths.remove_voter()
                    if latest_departure > t:
                        voter.start_time = latest_departure
                        voter.departure_time = latest_departure + voting_duration
                        booths.add_voter(voter.departure_time)
                    else:
                        voter.start_time = t
                        voter.departure_time = t + voting_duration
                        booths.add_voter(voter.departure_time)

                voter_count += 1
                gap, voting_duration = util.gen_voter_parameters(self.arrival_rate, self.voting_duration_rate, percent_straight_ticket, straight_ticket_duration=2)
                next_arrival = t + gap
                voters.append(voter)
            
            t = next_arrival

           
        return voters


### YOUR VotingBooths class GOES HERE.

class VotingBooths(object):
    '''
    Voting booths in a precinct
    '''
    def __init__(self, num_booths):
        '''
        Constructor

        Parameters:
            num_booths: (int) the number of booths in a precinct
        '''
        self.__pq = queue.PriorityQueue(maxsize = num_booths)

    def add_voter(self, departure_time):
        '''
        Adding a voter to the booth
        
        Input:
            departure_time: (float) time of departure
        
        Returns: None
        '''
        self.__pq.put(departure_time, block = False) 
    
    def remove_voter(self):
        '''
        Removes a voter from the booth
        
        Input: None
        
        Returns: (float) time of departure
        '''

        departure_time = self.__pq.get(block = False)

        return departure_time
    
    def is_empty(self):
        '''
        Check if voting booths are empty
        '''
        
        return self.__pq.empty()

    def is_full(self):
        '''
        Check if voting booths are full
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
    p = Precinct(name, hours_open, max_num_voters, num_booths, arrival_rate, voting_duration)
    
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
        
    # REPLACE 0.0 with the waiting time this function computes
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

    percent_split_ticket = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for percentage in percent_split_ticket:
        avg_wait_time = find_avg_wait_time(precinct, 1 - percentage, ntrials, seed)
        if avg_wait_time > target_wait_time:
            max_percent = percentage
            break
        elif percentage == 1 and avg_wait_time < target_wait_time:
            return (1, None)
         
    return (max_percent, avg_wait_time)


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
