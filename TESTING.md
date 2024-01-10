# Testing

## Manual Testing

Throughout the development of BarkBuddies, comprehensive testing was conducted to ensure each feature's functionality before integration into the master branch.

Various user acceptance tests were sent to new users. This aimed to gather feedback from diverse users on different devices and browsers, helping identify and fix issues during development.

|     | User Actions           | Expected Results | Y/N | Comments    |
|-------------|------------------------|------------------|------|-------------|
| Register     |                        |                  |      |             |
| 1           | Click on the Register button | Leads to page with registration form | Y |    Only for logged out users      |
| 2           | Enter valid username | Field will only accept up to 150 characters | Y |  
| 3           | Enter valid email | Field will only accept email address format | Y |          |
| 4           | Leave email field empty | As field is optional, the submission is still accepted | Y |          |
| 5          | Enter valid password | Field will only accept secure passwords | Y |          |
| 6          | Enter valid password confirmation | Field will only accept the same password from the previous field | Y |          |
| 7          | Click on the Register button | Leads user to home page with an alert message confirming successful registration. Register and Login buttons are replaced by My Bookings and Logout buttons. | Y |          |
| 8        | Click on Logout button | Takes user to log out page to confirm logout | Y |          |
| 9          | Click Logout button in the center of the page | Redirects user to home page with alert message confirming successful logout. Register and login buttons appear again. | Y |          |
| Log In      |                        |                  |      |             |
| 1           | Click on the Login button | Leads to page with Login form | Y |  Only for logged out users        |
| 2           | Enter valid username |  Field will only accept up to 150 characters | Y |          |
| 3           | Enter valid password | Field will only accept secure passwords | Y |          |
| 4           | Clicks  the optional “Remember Me” tickbox | Nothing happens right after ticking the box | Y |          |
| 5           | Click on the Login button | Takes user to the same page they have previously been on. User is shown a success alert confirming login. Register and Login buttons are replaced by My Bookings and Logout buttons.  | Y |          |
| 6        | Click on Logout button | Takes user to log out page to confirm logout | Y |          |
| 7          | Click Logout button in the center of the page | Redirects user to home page with alert message confirming successful logout. Register and login buttons appear again. | Y |          |
| Log Out      |                        |                  |      |             |
| 1           | Click on the Logout button | Leads to Log out confirmation page  | Y |      Only visible for logged in users    |
| 2           | Click on “Logout” button on center of the page |   Redirects user to home page with alert message confirming successful logout. Register and login buttons appear again. | 
Menu        |                        |                  |      |             |
| 1           | Click on the "BarkBuddies" logo | Redirection to Home page | Y | Available to everyone |
| 2           | Click on "Home" | Redirection to Home page | Y | Available to everyone |
| 3           | Click on "About" | Leads to About section on Home page | Y | Available to everyone |
| 4           | Click on "Testimonials" | Redirection to Reviews section on Home page | Y | Available to everyone |
| 5           | Click on "Services" | Dropdown menu with available Services appears | Y | Available to everyone |
| 6           | Click on any of the Services from the Dropdown menu | Redirection to Service Detail page | Y |  Available to everyone |
| 7           | Click on "My Bookings" (if logged in) | Redirection to Booking overview page | Y | Available to logged in users |
| Home page |            |                  |      |             |
| 1           |  Click on “Book a Service” button | User is navigated to service section of Home page  | Y |   |
| 2           |  Click on any Service card |  User is redirected to the Service Detail page of that service  | Y |   |
| 3           |  Click on “Want to leave a Review?” | The Review Modal opens | Y |  Available only for logged in users with a past booking.  |
| My Bookings page    |            |                  |      |             |
| 1           |  If Booking available, click on “Cancel” button underneath a Booking | Stay on the same page and an alert appears confirming cancellation. The booking is shown as cancelled with a Re-Book and Delete button. | Y | Available only to logged in users with a booking. Error appears if the user tries to cancel within 24 hours of appointment.  |
| 2           |  If Booking available, click on “Re-Book” button underneath a Booking | Redirect to the Service Detail page where users can place another booking. | Y |  Available only for logged in users with a booking.  |
| 3           |  If Booking cancelled, click on “Re-Book” button underneath a Booking | Redirect to the Service Detail page where users can place another booking. | Y |  Available only for logged in users with a cancelled booking.  |
| 4           |  If Booking cancelled, click on “Delete” button underneath a Booking | Stay on the same page and an alert appears confirming deletion. The booking disappears. If there are no bookings, a message stating that the user has no bookings appears. | Y |  Available only for logged in users with a cancelled booking.  |
| 5           |  Click on “Want to leave a Review?” | Review Modal opens. | Y |  Available only for logged in users with a past booking.  |
| Service Detail page |            |                  |      |             |
| 1           |  Click "Book Now" button underneath the Service text | Booking Modal for this Service opens | Y | Available only to logged in users  |
| 2           |  Click "Login to book Service" button underneath the Service text | User is redirected to login and is then redirected back to the Service Detail page. | Y | Only visible if not logged in  |
| 3           |  Click any of the other Service cards underneath | User is redirected to the Service Detail page of that service. | Y |   |
| Booking Modal |            |                  |      |             |
| 1           |  Click on “Calendar” Icon to select Start Date | Calendar for selection opens. Paste dates are automatically disabled.  | Y |   |
| 2           |  Click "One Day" checkmark | End date field is filled automatically with the same date as the start date. | Y |   |
| 3           |  Click on “Calendar” Icon to select End Date | Calendar for selection opens. Paste dates are automatically disabled. | Y | Only clickable if One Day check is not ticked.  |
| 4           |  Click on “Calendar” Icon to select End Date | Calendar for selection opens. Paste dates are automatically disabled. | Y | Only clickable if One Day check is not ticked.  |
| 5           |  Click on “Time” dropdown to select a timeslot | Dropdown with available times appears and time can be selected. Unavailable times are disabled. | Y |   |
| 6           |  Enter a comment | Field will only accept up to 400 characters. | Y |   |
| 7           |  Tick checkmark “Add Second Dog” | The total price will automatically change and add 50% of the price. | Y |   |
| 8           |  Click “Close” button | The booking modal closes and the user stays on the Service Detail page. | Y |   |
| 9           |  Click “Book Now” button | The booking modal closes and the user gets a confirmation alert for successful booking, or an error if unsuccessful. The booking is displayed on the page. | Y |   |
| Review Modal  |     |      |     |    |
| 1                | Click Service dropdown | Available Services appear and can be selected | Y |   |
| 2                | Enter a comment into Body field | Field will only accept up to 400 characters. | Y |   |
| 3                | Click “Submit” button | Modal is closed and user sees a success alert for the submitted comment.  | Y |  |
| Footer |            |                  |      |             |
| 1           |  Click on “Our Services” | User is navigated to service section of Home page  | Y |   |
| 2           |  Click on “Testimonials” |  User is redirected to the review section of Home page | Y |   |
| 3           |  Click on “Bookings” | User is redirected to My Bookings page | Y |  Available only for logged in users. Will be redirected to the Login page otherwise. |


## Testing User Story

## Bugs

### Known bugs

### Solved bugs

## Automated testing

### Django unit testing

- test_forms.py, test_models.py, test_views.py and test_urls.py
- While developing tests I was running the following command:

```
python manage.py test <name of the app>
```

To create the coverage report, I ran the following command:

```
coverage run --source=<name of the app> manage.py test
```

```
coverage report
```

To see the html version of the report, I ran the following command:

```
coverage html
```

```
    python3 -m http.server
```

The link to the server will appear. Click the link to see the report and find out which parts of code has not been covered in testing.

### Jest unit testing

## Validation

### HTML Validation

### CSS Validation

### JS Validation

### Python Validation

## Lighthouse Report

### All Pages

## Compatibility

Testing was conducted on the following browsers;

- Safari;
- Chrome;
- Firefox;

# Responsiveness

- Devtools
- Responsive Viewer
