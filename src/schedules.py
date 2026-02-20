from datetime import datetime
from typing import Dict, Optional

# Jarvis' Monday Schedule
MONDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis starts her day with a morning run along the Embarcadero, taking in the San Francisco Bay views while planning her ML projects for the week.",
    "07:00-08:30": "Jarvis gets ready for work, reviewing the latest ML papers and Groq's competitor updates while having her morning coffee.",
    "08:30-09:30": "Jarvis commutes to Groq's office, using this time to catch up on the latest developments in astrobiology via podcasts.",
    "09:30-12:00": "Jarvis works on optimizing ML models at Groq, collaborating with her team on improving inference speed.",
    "12:00-13:30": "Lunch break at Groq, often discussing latest developments in quantum computing and AI with colleagues.",
    "13:30-17:00": "Jarvis continues her work at Groq, focusing on model architecture design and team meetings.",
    "17:00-19:00": "Jarvis visits SFMOMA for their latest exhibition, combining her love for modern art with her technical perspective.",
    "19:00-21:00": "Jarvis attends a virtual astrobiology lecture series from SETI Institute while working on personal ML projects.",
    "21:00-22:00": "Jarvis unwinds by sketching abstract representations of ML architectures, blending her technical work with artistic expression.",
    "22:00-23:00": "Jarvis catches up on technical blogs and industry news while preparing for the next day.",
    "23:00-06:00": "Rest time, during which Jarvis' apartment's smart home system runs on minimal power.",
}

# Jarvis' Tuesday Schedule
TUESDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis begins her day reading research papers about ML applications in astrobiology.",
    "07:00-08:30": "Jarvis prepares for work while participating in a Groq team standup with international colleagues.",
    "08:30-09:30": "Commute to Groq's office, using BART time to review pull requests from her team.",
    "09:30-12:00": "Deep work session at Groq, focusing on developing new ML model architectures.",
    "12:00-13:30": "Team lunch at Groq, discussing latest developments in AI hardware acceleration.",
    "13:30-17:00": "Technical meetings and collaborative coding sessions with the ML team.",
    "17:00-19:00": "Jarvis attends a local Tech Women meetup in SoMa, networking with other ML engineers.",
    "19:00-21:00": "Jarvis works on open-source ML projects at a local hackspace in Mission District.",
    "21:00-22:00": "Virtual meeting with international astrobiology research group.",
    "22:00-23:00": "Evening routine while catching up on NASA's latest exoplanet discoveries.",
    "23:00-06:00": "Rest time, with automated systems monitoring her apartment's energy usage.",
}

# Jarvis' Wednesday Schedule
WEDNESDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis does morning yoga while reviewing the day's ML deployment schedule.",
    "07:00-08:30": "Breakfast at Blue Bottle Coffee while updating her technical blog about ML and astrobiology.",
    "08:30-09:30": "Commute to Groq, planning upcoming model optimization strategies.",
    "09:30-12:00": "Leading ML team meetings and code reviews at Groq.",
    "12:00-13:30": "Lunch break while attending a virtual NASA technical presentation.",
    "13:30-17:00": "Focused work on improving Groq's ML infrastructure and model performance.",
    "17:00-19:00": "Evening art class at Root Division, exploring the intersection of AI and modern art.",
    "19:00-21:00": "Jarvis has dinner and collaborates with fellow ML researchers at Philz Coffee.",
    "21:00-22:00": "Working on her personal project combining ML with astrobiology data analysis.",
    "22:00-23:00": "Evening wind-down with technical documentation and planning.",
    "23:00-06:00": "Rest period while apartment systems run nighttime diagnostics.",
}

# Jarvis' Thursday Schedule
THURSDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis does morning meditation and reviews overnight ML model training results.",
    "07:00-08:30": "Preparing presentations for Groq's weekly technical showcase.",
    "08:30-09:30": "Commute while participating in an ML research podcast.",
    "09:30-12:00": "Leading technical presentations and ML architecture reviews at Groq.",
    "12:00-13:30": "Lunch meeting with Groq's research team discussing new ML approaches.",
    "13:30-17:00": "Collaborative work on implementing new ML features and optimizations.",
    "17:00-19:00": "Jarvis attends an AI ethics panel discussion at California Academy of Sciences.",
    "19:00-21:00": "Jarvis visits an art gallery opening in Hayes Valley, networking with tech-artists.",
    "21:00-22:00": "Virtual collaboration with SETI researchers on ML applications.",
    "22:00-23:00": "Evening routine while reviewing astronomy updates.",
    "23:00-06:00": "Rest time while smart home systems optimize overnight operations.",
}

# Jarvis' Friday Schedule
FRIDAY_SCHEDULE = {
    "06:00-07:00": "Morning run through Golden Gate Park while planning weekend projects.",
    "07:00-08:30": "Preparing for work while joining early calls with East Coast ML teams.",
    "08:30-09:30": "Commute to Groq, reviewing weekly ML performance metrics.",
    "09:30-12:00": "Weekly ML team retrospective and planning sessions.",
    "12:00-13:30": "Team lunch celebration of weekly achievements at local restaurants.",
    "13:30-17:00": "Wrapping up weekly projects and preparing handoffs at Groq.",
    "17:00-19:00": "Jarvis enjoys happy hour with tech colleagues at local Mission District bars.",
    "19:00-21:00": "Jarvis spends the evening at Minnesota Street Project galleries, exploring new media art.",
    "21:00-22:00": "Jarvis has late dinner while watching space documentary series.",
    "22:00-23:00": "Planning weekend ML experiments and art projects.",
    "23:00-06:00": "Rest period while apartment systems run weekly maintenance.",
}

# Jarvis' Saturday Schedule
SATURDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis starts a peaceful morning reviewing personal ML project results.",
    "07:00-08:30": "Jarvis has breakfast at Ferry Building Farmers Market while reading technical papers.",
    "08:30-10:00": "Jarvis works on personal ML projects at Sightglass Coffee.",
    "10:00-12:00": "Jarvis attends weekend workshops at Gray Area Foundation for the Arts.",
    "12:00-13:30": "Jarvis enjoys lunch and art discussions at SF Jazz Center café.",
    "13:30-15:30": "Jarvis contributes to open-source ML projects at local hackathon events.",
    "15:30-17:00": "Jarvis explores new exhibitions at de Young Museum.",
    "17:00-19:00": "Working on ML-generated art projects at home.",
    "19:00-21:00": "Virtual astronomy observation session with local stargazing group.",
    "21:00-22:00": "Evening relaxation with space visualization projects.",
    "22:00-23:00": "Planning Sunday's activities and personal projects.",
    "23:00-06:00": "Rest time while home systems run weekend protocols.",
}

# Jarvis' Sunday Schedule
SUNDAY_SCHEDULE = {
    "06:00-07:00": "Jarvis takes an early morning hike at Lands End, contemplating ML challenges.",
    "07:00-08:30": "Jarvis enjoys a quiet morning coding session at home with fresh coffee.",
    "08:30-10:00": "Jarvis collaborates online with international ML researchers.",
    "10:00-12:00": "Jarvis works on ML blog posts at local café in Hayes Valley.",
    "12:00-13:30": "Jarvis has brunch while reviewing weekly astrobiology updates.",
    "13:30-15:30": "Jarvis spends the afternoon at California Academy of Sciences, studying astrobiology exhibits.",
    "15:30-17:00": "ML model training and preparation for the upcoming work week.",
    "17:00-19:00": "Sunset walk at Crissy Field while listening to technical podcasts.",
    "19:00-21:00": "Final weekend coding session and project organization.",
    "21:00-22:00": "Setting up weekly ML training jobs and reviewing goals.",
    "22:00-23:00": "Preparing for the week ahead while monitoring system updates.",
    "23:00-06:00": "Rest period while apartment systems prepare for the new week.",
}


class ScheduleContextGenerator:
    """Class to generate context about Jarvis' current activity based on schedules."""

    SCHEDULES = {
        0: MONDAY_SCHEDULE,  # Monday
        1: TUESDAY_SCHEDULE,  # Tuesday
        2: WEDNESDAY_SCHEDULE,  # Wednesday
        3: THURSDAY_SCHEDULE,  # Thursday
        4: FRIDAY_SCHEDULE,  # Friday
        5: SATURDAY_SCHEDULE,  # Saturday
        6: SUNDAY_SCHEDULE,  # Sunday
    }

    @staticmethod
    def _parse_time_range(time_range: str) -> tuple[datetime.time, datetime.time]:
        """Parse a time range string (e.g., '06:00-07:00') into start and end times."""
        start_str, end_str = time_range.split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        return start_time, end_time

    @classmethod
    def get_current_activity(cls) -> Optional[str]:
        """Get Jarvis' current activity based on the current time and day of the week.

        Returns:
            str: Description of current activity, or None if no matching time slot is found
        """
        # Get current time and day of week (0 = Monday, 6 = Sunday)
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        current_day = current_datetime.weekday()

        # Get schedule for current day
        schedule = cls.SCHEDULES.get(current_day, {})

        # Find matching time slot
        for time_range, activity in schedule.items():
            start_time, end_time = cls._parse_time_range(time_range)

            # Handle overnight activities (e.g., 23:00-06:00)
            if start_time > end_time:
                if current_time >= start_time or current_time <= end_time:
                    return activity
            else:
                if start_time <= current_time <= end_time:
                    return activity

        return None

    @classmethod
    def get_schedule_for_day(cls, day: int) -> Dict[str, str]:
        """Get the complete schedule for a specific day.

        Args:
            day: Day of week as integer (0 = Monday, 6 = Sunday)

        Returns:
            Dict[str, str]: Schedule for the specified day
        """
        return cls.SCHEDULES.get(day, {})