from datetime import datetime

class ServiceRequest:
    next_ticket_id = 1

    def __init__(self, customer_name, priority, description):
        self.ticket_id = str(ServiceRequest.next_ticket_id).zfill(2)
        ServiceRequest.next_ticket_id += 1
        self.customer_name = customer_name
        self.priority = priority
        self.description = description
        self.status = "open"  # default status
        self.creation_time = datetime.now()
        self.close_time = None

    def set_status(self, status):
        self.status = status

    def set_close_time(self, close_time):
        self.close_time = close_time


class Node:
    def __init__(self, customer_name=None, priority=None, description=None):
        self.req = ServiceRequest(customer_name, priority, description)
        self.next = None

    def set_next(self, next_node):
        self.next = next_node

    def get_next(self):
        return self.next

    def get_id(self):
        return self.req.ticket_id if self.req else None

    def get_name(self):
        return self.req.customer_name if self.req else None

    def get_priority(self):
        return self.req.priority if self.req else None

    def get_status(self):
        return self.req.status if self.req else None

    def set_status(self, status):
        if self.req:
            self.req.set_status(status)

    def get_description(self):
        return self.req.description if self.req else None

    def get_creation_time(self):
        return self.req.creation_time if self.req else None

    def set_close_time(self, close_time):
        if self.req:
            self.req.set_close_time(close_time)

    def get_close_time(self):
        return self.req.close_time if self.req else None

    def print_time(self, time):
        if time:
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("No time available")

    # Methods to get and set the service_request object
    def get_request(self):
        return self.req

    def set_request(self, new_request):
        self.req = new_request


class TicketsList:
    def __init__(self):
        self.head = None
        self.tail = None

    def get_head(self):
        return self.head

    def add_ticket(self, customer_name, priority, description):
        new_node = Node(customer_name, priority, description)

        if self.head is None:  # List is empty
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.set_next(new_node)
            self.tail = new_node


    def print_tickets(self):
        current = self.head

        if current is None:
            print("No tickets to display.")
            return

        # Traverse and print details
        while current is not None:
            print(f"Ticket ID: {current.get_id()}")
            print(f"Customer Name: {current.get_name()}")
            print(f"Priority: {current.get_priority()} (1=High, 2=Medium, 3=Low)")
            print(f"Service Request: {current.get_description()}")
            print("Creation Time: ", end="")
            current.print_time(current.get_creation_time())
            print(f"Status: {current.get_status()}")

            if current.get_status() == "closed":
                print("Ticket Close Time: ", end="")
                current.print_time(current.get_close_time())

            print("-----------------------------")
            current = current.get_next()

    def open_tickets(self):
        current = self.head

        if current is None:
            print("There are no tickets in the list.")
            return

        while current is not None:
            if current.get_status() == "open":
                print(f"Ticket ID: {current.get_id()}")
                print(f"Customer Name: {current.get_name()}")
                print(f"Priority: {current.get_priority()} (1=High, 2=Medium, 3=Low)")
                print(f"Service Request: {current.get_description()}")
                print("Creation Time: ", end="")
                current.print_time(current.get_creation_time())
                print(f"Status: {current.get_status()}")

                print("-----------------------------")
            current = current.get_next()



class PendingTicketQueue:
    class QueueNode:
        def __init__(self, ticketID, priority, creationTime):
            self.ticketID = ticketID
            self.priority = priority
            self.creationTime = creationTime
            self.next = None

    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, ticketID, priority, creationTime):
        new_node = self.QueueNode(ticketID, priority, creationTime)
        if not self.front or (self.front.priority > priority) or \
           (self.front.priority == priority and self.front.creationTime > creationTime):
            new_node.next = self.front
            self.front = new_node
            if not self.rear:
                self.rear = self.front
        else:
            current = self.front
            while current.next and \
                  (current.next.priority < priority or 
                   (current.next.priority == priority and current.next.creationTime <= creationTime)):
                current = current.next
            new_node.next = current.next
            current.next = new_node
            if not new_node.next:
                self.rear = new_node
  

    def get_front(self):
        return self.front

    def is_empty(self):
         return self.front is None  # Returns True if the queue is empty, False otherwise
    # def get_front_ticket_id(self):
    #      return self.front.ticketID if self.front else -1
    def print_time(self, time):
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

    def display(self):
        current = self.front
        print("\nPending Tickets Queue (by priority and arrival):")
        if self.is_empty():
            print("NO Pending Queries !")
        while current:
            print(f"Ticket ID: {current.ticketID}, Priority: {current.priority}")
            print("Creation Time:", end=" ")
            self.print_time(current.creationTime)
            print()
            current = current.next


class TicketResolutionLogStack:
    class LogNode:
        def __init__(self, ticketID, resolutionInfo):
            self.ticketID = ticketID
            self.resolutionInfo = resolutionInfo
            self.next = None

    def __init__(self):
        self.top = None

    def push(self, ticketID, resolutionInfo):
        new_node = self.LogNode(ticketID, resolutionInfo)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return  # Stack is empty, nothing to pop
        temp = self.top
        self.top = self.top.next
        del temp  # Free the memory, though Python handles this automatically

    def display(self):
        current = self.top
        print("\nTicket Resolution Log (Most recent first):")
        if not current:
            print("No logs available.")
        while current:
            print(f"Ticket ID: {current.ticketID}, Resolution: {current.resolutionInfo}")
            current = current.next

class NADRA_ASSISTANT_CENTER:
    def __init__(self):
        self.ticket_list = TicketsList()
        self.pending_queue = PendingTicketQueue()

    def customer_menu(self):
        while True:
            print("\n Welcome to NADRA Assistant Center ")
            print("\n*******  Customer Menu  *********")
            print("\n1. Create a Ticket")
            print("2. View Pending Tickets")
            print("3. Close a Ticket")
            print("4. View Resolve Tickets ")
            print("5. View Open Tickets ")
            print("6. View All Tickets")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_ticket()
            elif choice == '2':
                self.view_pending_tickets()
            elif choice == '3':
                self.close_ticket()
            elif choice == '4':
                self.display_resolution_stack()
            elif choice == '5':
                self.open_tickets()
            elif choice == '6':
                self.view_all_tickets()
            elif choice == '7':
                break
            else:
                print("Invalid choice, please try again.")

    def create_ticket(self):
     print("\nSelect a NADRA Facility:")
     facilities = {
        1: ("New CNIC Registration", 1),
        2: ("Lost CNIC", 1),
        3: ("Urgent Passport Issuance", 1),
        4: ("CNIC Renewal", 2),
        5: ("CNIC Correction", 2),
        6: ("Document Verification", 2),
        7: ("Family Registration", 3),
        8: ("Birth/Marriage Certificate", 3)
     }

     while True:  # Keep prompting until valid input
        for key, (facility, priority) in facilities.items():
            print(f"{key}. {facility} (Priority {priority})")

        try:
            choice = int(input("Enter your choice: "))
            if choice not in facilities:
                print("Invalid choice. Please try again.")
                continue  # Go back to the start of the loop

            # Valid choice, proceed with ticket creation
            facility_name, priority = facilities[choice]
            customer_name = input("Enter your name: ")
            description = f"{facility_name} service requested"

            # Create ticket and enqueue
            self.ticket_list.add_ticket(customer_name, priority, description)
            self.pending_queue.enqueue(self.ticket_list.tail.get_id(), priority, self.ticket_list.tail.get_creation_time())
            print(f"Ticket created successfully!")
            print(f"Ticket ID: {self.ticket_list.tail.get_id()}")
            print(f"Facility: {facility_name}")
            print(f"Priority: {priority}")
            break  # Exit the loop after successful ticket creation

        except ValueError:
            print("Invalid input. Please enter a number.")


    def display_resolution_stack(self):
        if not hasattr(self, "resolution_stack"):  # Check if the stack exists
            print("No resolution log stack found.")
            return

        self.resolution_stack.display()

    def view_pending_tickets(self):
        self.pending_queue.display()

    def close_ticket(self):
        ticket_id = input("Enter the ticket ID to close: ")
        found = False

     # Step 1: Update ticket status in the ticket list
        current_ticket = self.ticket_list.get_head()
        while current_ticket is not None:
         if current_ticket.get_id() == ticket_id:
            current_ticket.set_status("closed")
            current_ticket.set_close_time(datetime.now())
            found = True
            break
         current_ticket = current_ticket.get_next()

        if not found:
         print(f"Ticket {ticket_id} not found.")
         return

    # # Step 2: Remove the ticket from the Qeueu
       
        if self.pending_queue.is_empty():
         print("No tickets in the queue to process.")
         return

        prev = None
        current = self.pending_queue.get_front()
        while current:
          if current.ticketID == ticket_id:
            if prev:
                prev.next = current.next
            else:
                self.pending_queue.front = current.next  # Update the front if it's the first ticket
            if current == self.pending_queue.rear:
                self.pending_queue.rear = prev  # Update rear if it's the last ticket
            print(f"Ticket {ticket_id} has been closed and removed from the queue.")
            break
          prev = current
          current = current.next
               

    # Step 3: Push the ticket into the resolution log stack
        if not hasattr(self, "resolution_stack"):  
         self.resolution_stack = TicketResolutionLogStack()

        self.resolution_stack.push(ticket_id, "Resolved and closed.")
        print(f"Ticket {ticket_id} has been pushed into the resolution log stack.")

   
        print(f"Ticket {ticket_id} has been closed successfully.")

    def open_tickets(self):
        self.ticket_list.open_tickets()

    def view_all_tickets(self):
        self.ticket_list.print_tickets()

    def start(self):
        self.customer_menu()

if __name__ == "__main__":
    system = NADRA_ASSISTANT_CENTER()
    system.start()
