
FlowChart

Admin Flow:

```mermaid
graph TD;
    Admin-->Login?;
    Login?--Yes-->AccessOptions;
    Login?--No-->CanAccessHome;
    AccessOptions-->ControlUnavailability;
    AccessOptions-->ControlServices;
    AccessOptions-->ControlBookings;
    AccessOptions-->ControlComments;
    AccessOptions-->ControlUsers;
    AccessOptions-->Home;
    CanAccessHome-->Home;
    CanAccessHome-->Register;
    Home-->AboutSection,ServiceOverview,Reviews;
    Register-->SignUp;
    ControlUsers--->Add/Delete;
    ControlUsers-->SortByName;
    ControlComments--->Add/Delete;
    ControlComments-->Review/Approve;
    ControlBookings--->Add/Delete;
    ControlBookings-->SortByDate/Title;
    ControlBookings-->Cancel;
    ControlServices--->Add/Delete;
    ControlServices-->SortByTitle;
    ControlUnavailability--->Add/Delete;
    ControlUnavailability-->SortByDate;
```

User Flow:

```mermaid
graph TD;
    User-->Login?;
    Login?--Yes-->AccessOptions;
    Login?--No-->CanAccessHome;
    AccessOptions-->Reviews;
    AccessOptions-->Booking;
    AccessOptions-->ServiceDetail;
    AccessOptions-->Home;
    CanAccessHome-->Home;
    CanAccessHome-->Register;
    Home-->AboutSection,ServiceOverview,Reviews;
    AboutSection,ServiceOverview,Reviews-->ClickService;
    AboutSection,ServiceOverview,Reviews-->CommentsDisabled;
    ClickService-->ServiceDetail;
    Register-->SignUp;
    Reviews--->AddComment;
    AddComment-->Approved?;
    Approved?--Yes-->PostComment;
    Approved?--No-->DeleteComment;
    Booking-->DeleteService;
    Booking-->CancelService;
    Booking-->RebookService;
    RebookService-->BookService
    DeleteService-->RemoveBooking;
    CancelService-->MarkAsCanceled;
    ServiceDetail-->BookService;
    BookService-->LoggedIn?;
    LoggedIn?--Yes-->AvailabilityCheck;
    LoggedIn?--No-->SignUp/LogIn;
    AvailabilityCheck--Failure-->Error;
    AvailabilityCheck--Success-->ForwardToBooking;
    ForwardToBooking-->Booking;
```

---
Credits

Illustrations: <https://www.freepik.com/search?author=10171402&authorSlug=pch.vector&format=author&query=dog>


----

## Codeanywhere Reminders

To run a frontend (HTML, CSS, Javascript only) application in Codeanywhere, in the terminal, type:

`python3 -m http.server`

A button should appear to click: _Open Preview_ or _Open Browser_.

To run a frontend (HTML, CSS, Javascript only) application in Codeanywhere with no-cache, you can use this alias for `python3 -m http.server`.

`http_server`

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A button should appear to click: _Open Preview_ or _Open Browser_.

In Codeanywhere you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to _Account Settings_ in the menu under your avatar.
2. Scroll down to the _API Key_ and click _Reveal_
3. Copy the key
4. In Codeanywhere, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.

---

Happy coding!
