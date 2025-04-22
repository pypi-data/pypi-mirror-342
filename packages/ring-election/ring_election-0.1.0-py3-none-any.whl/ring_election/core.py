import time
import random
import threading
from enum import Enum

class ProcessState(Enum):
    NORMAL = "NORMAL"
    PARTICIPANT = "PARTICIPANT"
    LEADER = "LEADER"

class Message:
    def __init__(self, message_type, sender_id, election_ids=None):
        self.type = message_type  # "ELECTION" or "COORDINATOR"
        self.sender_id = sender_id
        self.election_ids = election_ids if election_ids else []
    
    def __str__(self):
        if self.type == "ELECTION":
            return f"ELECTION{self.election_ids}"
        else:
            return f"COORDINATOR({self.sender_id})"

class Process:
    def __init__(self, process_id):
        self.id = process_id
        self.state = ProcessState.NORMAL
        self.leader_id = None
        self.active = True
        self.lock = threading.Lock()
        self.no_response_count = 0
    
    def __str__(self):
        return f"Process {self.id} (State: {self.state.value}, Leader: {self.leader_id})"

class RingNetwork:
    def __init__(self, num_processes):
        # Create processes with unique IDs
        self.processes = [Process(i) for i in range(num_processes)]
        self.num_processes = num_processes
        self.election_in_progress = False
        self.network_lock = threading.Lock()
        print(f"Created ring network with {num_processes} processes")
        
    def get_next_process(self, current_id):
        """Get the next process in the ring"""
        next_id = (current_id + 1) % self.num_processes
        return self.processes[next_id]
    
    def detect_coordinator_failure(self, process_id):
        """Process detects that the coordinator is not responding"""
        process = self.processes[process_id]
        print(f"\nProcess {process_id} detected that coordinator (Process {process.leader_id}) has crashed")
        self.initiate_election(process_id)
    
    def initiate_election(self, starter_id):
        """Initiate an election from a specific process using Chang and Roberts algorithm"""
        with self.network_lock:
            if self.election_in_progress:
                print(f"Election already in progress, Process {starter_id} will wait")
                return
            self.election_in_progress = True
            
        starter_process = self.processes[starter_id]
        
        with starter_process.lock:
            print(f"\nProcess {starter_id} initiates election")
            starter_process.state = ProcessState.PARTICIPANT
            
        # Start the election message with just the initiator's ID
        message = Message("ELECTION", starter_id, [starter_id])
        self.pass_election_message(starter_id, message)
    
    def pass_election_message(self, current_id, message):
        """Pass the election message to the next process in the ring"""
        current_process = self.processes[current_id]
        next_process = self.get_next_process(current_id)
        
        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.3))
        
        with next_process.lock:
            if not next_process.active:
                # If the next process is inactive, skip it
                print(f"Process {next_process.id} is inactive, skipping")
                # Try the next process in the ring
                self.pass_election_message(next_process.id, message)
                return
            
            print(f"Process {current_id} passes {message} to Process {next_process.id}")
            
            if message.type == "ELECTION":
                if next_process.id in message.election_ids:
                    # Process has received its own election message back
                    # It declares itself as the leader
                    highest_id = max(message.election_ids)
                    print(f"Process {next_process.id} received its own election message back")
                    print(f"The highest ID in the message is {highest_id}")
                    
                    # Create a coordinator message to announce the leader
                    coordinator_message = Message("COORDINATOR", highest_id)
                    self.pass_coordinator_message(next_process.id, coordinator_message)
                    return
                
                # According to Chang and Roberts Algorithm:
                # If the process's ID is greater than any in the message, it adds its ID
                # Otherwise, it forwards the message unchanged
                process_id = next_process.id
                max_id_in_msg = max(message.election_ids)
                
                if process_id > max_id_in_msg:
                    # Add this process ID to the message
                    print(f"Process {process_id} adds its ID to the election message")
                    new_ids = message.election_ids.copy()
                    new_ids.append(process_id)
                    new_message = Message("ELECTION", process_id, new_ids)
                    next_process.state = ProcessState.PARTICIPANT
                    self.pass_election_message(next_process.id, new_message)
                else:
                    # Forward the message unchanged
                    next_process.state = ProcessState.PARTICIPANT
                    self.pass_election_message(next_process.id, message)
            
    def pass_coordinator_message(self, current_id, message):
        """Pass the coordinator message around the ring"""
        current_process = self.processes[current_id]
        next_process = self.get_next_process(current_id)
        
        # Update current process with the new leader
        with current_process.lock:
            if current_process.id == message.sender_id:
                current_process.state = ProcessState.LEADER
            else:
                current_process.state = ProcessState.NORMAL
            current_process.leader_id = message.sender_id
        
        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.3))
        
        with next_process.lock:
            if not next_process.active:
                # If the next process is inactive, skip it
                print(f"Coordinator message: Process {next_process.id} is inactive, skipping")
                self.pass_coordinator_message(next_process.id, message)
                return
            
            print(f"Process {current_id} informs Process {next_process.id} that Process {message.sender_id} is the new coordinator")
            
            # Update this process with the new leader
            if next_process.id == message.sender_id:
                next_process.state = ProcessState.LEADER
            else:
                next_process.state = ProcessState.NORMAL
            next_process.leader_id = message.sender_id
            
            # If we've made a full circle (back to the original sender), we're done
            if next_process.id == message.sender_id:
                print(f"\n*** Process {message.sender_id} has been elected as LEADER ***\n")
                with self.network_lock:
                    self.election_in_progress = False
                return
            
            # Continue passing the coordinator message
            self.pass_coordinator_message(next_process.id, message)
    
    def crash_process(self, process_id):
        """Simulate a process crash"""
        if process_id < 0 or process_id >= self.num_processes:
            print(f"Invalid process ID: {process_id}")
            return
            
        process = self.processes[process_id]
        with process.lock:
            process.active = False
            print(f"\n!!! Process {process_id} has crashed !!!")
            
        # If the crashed process was the leader, a process that communicates with it will 
        # eventually detect the failure and start an election
        if process.state == ProcessState.LEADER:
            # Simulate another process detecting the failure
            detector_id = (process_id - 1) % self.num_processes
            while not self.processes[detector_id].active:
                detector_id = (detector_id - 1) % self.num_processes
            
            print(f"Process {detector_id} will detect that leader has crashed")
            # Schedule the detection after a short delay
            threading.Timer(1.0, self.detect_coordinator_failure, [detector_id]).start()
    
    def recover_process(self, process_id):
        """Recover a crashed process"""
        if process_id < 0 or process_id >= self.num_processes:
            print(f"Invalid process ID: {process_id}")
            return
            
        process = self.processes[process_id]
        with process.lock:
            if not process.active:
                process.active = True
                process.state = ProcessState.NORMAL
                process.leader_id = None
                print(f"\n!!! Process {process_id} has recovered !!!")
                # Recovered process initiates an election
                threading.Timer(0.5, self.initiate_election, [process_id]).start()
    
    def display_status(self):
        """Display the status of all processes"""
        print("\n----- Network Status -----")
        for process in self.processes:
            with process.lock:
                status = f"Process {process.id}: {process.state.value}"
                if process.leader_id is not None:
                    status += f", Leader: {process.leader_id}"
                if not process.active:
                    status += " [INACTIVE]"
                print(status)
        print("------------------------\n")


def main():
    # Create a ring network with 7 processes (0-6) as shown in the image
    network = RingNetwork(7)
    
    # Set process 7 as the initial leader (previous coordinator)
    # Since we're using 0-based indexing and only have processes 0-6,
    # we'll simulate this by just saying process 6 knows process 7 was the leader
    process6 = network.processes[6]
    with process6.lock:
        process6.leader_id = 7  # This represents the crashed coordinator 7
    
    # Display initial status
    network.display_status()
    
    # Process 6 detects that process 7 (coordinator) has crashed and starts an election
    print("Simulating: Process 6 detected that Process 7 (coordinator) is not responding")
    network.initiate_election(2)  # Start with process 2 as in the diagram
    
    # Wait for the election to complete
    time.sleep(4)
    
    # Display status after election
    network.display_status()
    
    # Crash the new leader
    for process in network.processes:
        if process.state == ProcessState.LEADER:
            network.crash_process(process.id)
            break
    
    # Wait for the new election to complete
    time.sleep(4)
    
    # Display status after leader crash and re-election
    network.display_status()

if __name__ == "__main__":
    main()