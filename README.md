# Keepgate
An event ticketing system written for the University of Helsinki Database lab in Autumn 2021

## Planned features
Keepgate is an event ticket management application that helps users to keep track of invites to e.g. parties. Users can set up events and create entrance tickets that other users present at the door. The event organiser can create different ticket types for their events, check the ticket validity (does the ticket exist and has it already been used), and update already sent tickets (e.g. change names that are displayed on the ticket or invalidate tickets remotely).

The UI will consist of a control panel for users to set up events and manage tickets, a ticket view that event-goers present at the door, and a ticket-checking view where a doorkeeper can check ticket validity.

The ticket view has the ticket identifier both as text and as a QR code (that points to an address like https://keepgate.fi/check/134234) and optional additional info (e.g. the name of the ticket holder). The ticket checking view will show a copy of the ticket (since you can't trust anything on the event-goers' device) and whether the ticket has already been used.

## Current features
The app is hosted at https://tsoha-keepgate.herokuapp.com. No interactive functionality has been implemented yet, most of my time's been used on making Postgres, Heroku, and Tailwind work at all. At the moment there's some manually inserted test data in the database, and the front page of the app simply demonstrates that the db-connection is working. On the back-end, some of the database related functions are complete already, some still have hard-coded values I've used for testing, and some are yet to be written.