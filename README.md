# Keepgate
An event ticketing system written for the University of Helsinki Database lab in Autumn 2021

With Keepgate you can create virtual tickets for your events. Guests show their ticket at the door, and an event organiser scans the QR code on the ticket to validate it. Keepgate also features passes that hold values which the event organisers can add or deduct from.

## Features as a list
* Users can log in to create and organise events
* Event owners can manage tickets, passes, and organisers for their events
* Event owners can see the statuses of tickets (stamped or unstamped, stamped by whom), the values held by passes and the transactions that have taken place (additions/deductions and by whom)
* Event owners can add extra information for the event that'll be shown on all tickets and passes
* Event owners can add extra information for individual tickets or passes that will be shown with the ticket/pass
* Users designated as organisers for events can stamp tickets and add/deduct value on passes
* Guests can show their tickets/passes on their phones, and organisers can scan the codes to stamp/manage

## Quick start to get the gist
Event owner:
1. Create an account and an event.
2. Create a ticket and share the link to it to a guest (send it to a friend).
Event organiser:
3. Create an account and tell the account name to the event owner
Event owner:
4. Add the organiser to your event and give them permission to stamp tickets
Event organiser:
5. Log in to keepgate on your phone
Guest:
6. Open the ticket on your phone and show it to the event organiser
Event organiser:
7. Scan the QR code on the guest's phone and follow the link
8. You will see a green "valid" screen, telling you the ticket hasn't been stamped yet.
9. Now that you've scanned the ticket, the ticket has been stamped — the ticket will auto-update itself to reflect this.
10. Scan the ticket again.
11. You will see a yellow "stamped" screen, telling you that the ticket has already been stamped
Event owner:
12. Look at the ticket page for your event to see that the ticket has been stamped.
13. Open the ticket details to see who stamped the ticket.

## Cut features
I originally planned for organisers to be able to _unstamp_ tickets but had to cut that feature due to a lack of time in the end. Organisers were also supposed to be able to create and remove tickets/passes just like an owner but, again, lack of time. And lastly, tickets and passes were supposed to be able to be "locked" to certain users, requiring a log in before they would display. These planned features haunt the code, so don't get spooked.