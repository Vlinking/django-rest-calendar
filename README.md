# django-rest-calendar
A calendar with monthly, weekly, daily views made using Django and REST API framework

## Functionality

- each user may use a different time zone
- event has a title and a description
- event always belongs to a single calendar
- calendar always has a single owner (user)
- calendar has a user-specified name
- calendar has a user-specified color
- there are two ways to provide event's start/end date and time - "all day" or normal
- all-day events are not timezone aware - they span whole day regardless of user's timezone
- normal events have timezone aware start and end date and time
- user has the ability to specify timezone for normal events
- event always has start and end date (and time in case of normal events)
- calendar may be shared with other users of the system
- two levels of access: read and write
- write access allows for modification of all events in that calendar
- event can have a list of guests - other users of the app
- users invited to event see the event in their calendar app
- guest user is able to edit an event, but only that guest sees those changes
- guest user can edit name, description start and end date/time and can switch between all-day and normal event
- guest or an owner is able to RSVP (there are four possible states - unknown, maybe, yes and no)
