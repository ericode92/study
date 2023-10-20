import flet
from flet import *
import calendar
import datetime

# some contents
cell_size = (28, 28)
cell_bg_color = "white10"
today_bg_color = "teal600"

# let's start first with the actual calendar control. We'll tackle the UI a bit and focus heavy on the logic.
class SetCalendar(UserControl):
    def __init__(self, start_year=datetime.date.today().year):
        # we'll need a few class instances up here first.
        # this widget will display the 12 months of year 2023. But it an additional instance can be added to display other years as well.
        self.current_year = start_year # the current year

        self.m1 = datetime.date.today().month # current month
        self.m2 = self.m1 + 1 # the second month, needed for the calendar module

        self.click_count: list = [] # for tracking clicks
        self.long_press_count: list = [] # same as above

        self.current_color = "blue" # highlight color

        self.selected_date = any # the selected data from the calendar

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        super().__init__()

    # first, let's create the ability to paginate the months
    def _change_month(self, delta):
        # recall that we stored the current month + month2 above as self.m1 and self.m2
        # we can use the max and min to make sure the numbers stay between 1 and 13, as per the calendar library
        
        # the below now keeps m1 between 1 and 12, and m2 between 2 and 13.
        self.m1 = min(max(1, self.m1 + delta), 12)
        self.m2 = min(max(2, self.m2 + delta), 13)

        # we need to create a new calendar variable
        new_calendar = self.create_month_calendar(self.current_year)
        self.calendar_grid = new_calendar
        self.update() # this should update the calendar by month

    # finally, we can keep adding more functions to make the widget more complex. Let's highlight the container when it's clicked.
    def one_click_date(self, e):
        # if we want to change the text title to the highlighted click, we can also do this...but it'll require a third button.
        self.selected_date = e.control.data
        e.control.bgcolor = "blue600"
        e.control.update()
        self.update()

    def long_click_date(self, e):
        # now for multiple dates.
        # we can set this up so that a user can click two dates and it'll highlight all the dates in between.

        # 1. save the two clicks to a list
        self.long_press_count.append(e.control.data)
        # 2. check to see if there are indeed 2 clicks
        if len(self.long_press_count) == 2:

            # 3. set two dates by unpacking the list
            date1, date2 = self.long_press_count

            # 4. get the absolute distance between them
            delta = abs(date2 - date1)

            # 5. now check to see if it's past selection or future
            if date1 < date2:
                dates = [
                    date1 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]
            else:
                dates = [
                    date2 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]

            # 6. we loop over the calendar matrix and color the boxes
            for _ in self.calendar_grid.controls[:]:
                for __ in _.controls[:]:
                    if isinstance(__, Row):
                        for box in __.controls[:]:
                            # 7. here we check to see if the dates list above matches the dates we created for each container's data
                            if box.data in dates:
                                box.bgcolor = "blue600"
                                box.update()

            self.long_press_count = []
        else:
            pass

    # we can now create the logic for the calendar
    def create_month_calendar(self, year):
        self.current_year = year # we get the current year
        self.calendar_grid.controls: list = [] # clear the calendar grid

        for month in range(self.m1, self.m2):
            # this gets the month name + year
            month_label = Text(
                f"{calendar.month_name[month]} {self.current_year}",
                size=14,
                weight="bold",
                color="white" # color added (since it's not Mac OS)
            )

            # now we need a month matrix
            # this gets the days of the month as per the year passed in
            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START, controls=[month_label],
                )
            )

            # now let's get the weekday labels
            # this is in the form of list. compr.
            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color="white70",
                    ),
                )
                for weekday in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            ]

            # now put the list of weekday containers in a row
            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            # now for the days
            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day == 0: # if the day in the grid is empty
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=border.all(0.5, "white24"),
                            alignment=alignment.center,
                            # we need to pass in some additional parameters to the main day cont.
                            # we use this data for the above!
                            data=datetime.date(
                                year=self.current_year, month=month, day=day
                            ),
                            on_click=lambda e: self.one_click_date(e),
                            on_long_press=lambda e: self.long_click_date(e),
                            animate=400,
                        )
                    day_label = Text(str(day), size=12, color="white")

                    # we need to make a second check here
                    if day == 0:
                        day_label = None
                    if (
                        day == datetime.date.today().day
                        and month == datetime.date.today().month
                        and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = "teal700"
                    day_container.content = day_label
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)
        
        self.calendar_grid.controls.append(month_grid)

        return self.calendar_grid

    def build(self):
        return self.create_month_calendar(self.current_year)


# let's switch and get to the upper level UI
class DateSetUp(UserControl):
    def __init__(self, cal_grid):
        self.cal_grid = cal_grid # this is the calendar instance

        # we can now create the buttons here
        self.prev_btn = BTNPagination("Prev", lambda e: cal_grid._change_month(-1))
        self.next_btn = BTNPagination("Next", lambda e: cal_grid._change_month(1))

        self.today = Text(
            datetime.date.today().strftime("%B %d, %Y"),
            width=260,
            size=13,
            color="white54",
            weight="w400"
        )

        # this will hold the pagination button
        self.btn_container = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                # button go in here
                self.prev_btn,
                self.next_btn
            ],
        )

        # this container will store the calendar you see to the right.
        self.calendar = Container(
            width=320,
            height=45,
            bgcolor="#313131",
            border_radius=8,
            animate=300,
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # here, we can pass in the actual calendar instance plus the buttons
                    Divider(height=60, color='transparent'),
                    self.cal_grid,
                    Divider(height=10, color='transparent'),
                    self.btn_container,
                ],
            ),
        )

        super().__init__()

    # we need a function to expand the stack to see the calendar
    def _get_calendar(self, e:None):
        if self.calendar.height == 45:
            self.calendar.height = 450
            self.calendar.update()
        else:
            self.calendar.height = 45
            self.calendar.update()
        pass

    def build(self):
        return Stack(
            # use a stack to stack the controls on top of each other
            width=320,
            controls=[
                self.calendar,
                Container(
                    on_click=lambda e: self._get_calendar(e),
                    width=320,
                    height=45,
                    border_radius=8,
                    bgcolor="#313131",
                    padding=padding.only(left=15, right=5),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.today,
                            Container(
                                width=32,
                                height=32,
                                border=border.only(
                                    left=BorderSide(0.9, "white24"),
                                ),
                                alignment=alignment.center,
                                content=Icon(
                                    name=icons.CALENDAR_MONTH_SHARP,
                                    size=15,
                                    opacity=0.7,
                                    color="white"
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )
    

# let's divert quickly and create the buttons for pagination
class BTNPagination(UserControl):
    def __init__(self, txt_name, function):
        self.txt_name = txt_name
        self.function = function
        super().__init__()

    def build(self):
        return IconButton(
            content=Text(self.txt_name, size=9, weight="bold"),
            width=56,
            height=28,
            on_click=self.function,
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=5)}, bgcolor={"": "teal600"}
            ),
        )

#main function
def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "top_center"
    page.padding = 80
    page.bgcolor = "#151515"

    # instances
    cal = SetCalendar()
    date = DateSetUp(cal)

    # main UI place
    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                date,
            ]
        )
    )
    page.update()


if __name__ == "__main__":
    flet.app(target=main)