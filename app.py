import streamlit as st
import pandas as pd

# --- Grade Point Mapping ---
# Using a standard 4.0 scale. You can adjust this dictionary 
# if your institution uses a different scale.
GRADE_POINTS = {
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0
}
GRADE_OPTIONS = list(GRADE_POINTS.keys())

# --- GPA Calculator Function (Single Semester) ---
def gpa_calculator():
    st.title("GPA Calculator (Single Semester)")
    st.write("Enter your courses, credits, and grades for this semester.")

    # Get the number of courses
    num_courses = st.number_input("How many courses did you take?", min_value=1, value=4)

    courses = []
    total_points = 0.0
    total_credits = 0.0

    # Create input fields for each course
    for i in range(num_courses):
        st.write(f"--- Course {i+1} ---")
        # Use columns for a cleaner layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Input for credit hours
            credits = st.number_input(
                f"Course {i+1} Credit Hours", 
                min_value=1, 
                max_value=6, 
                value=3, 
                key=f"credits_{i}"
            )
        
        with col2:
            # Input for grade
            grade = st.selectbox(
                f"Course {i+1} Grade", 
                options=GRADE_OPTIONS, 
                key=f"grade_{i}"
            )
        
        # Store data
        courses.append({'Course': f"Course {i+1}", 'Credits': credits, 'Grade': grade})
        
        # Calculate points for this course
        points = GRADE_POINTS[grade] * credits
        total_points += points
        total_credits += credits

    # Calculate GPA
    if st.button("Calculate GPA"):
        if total_credits > 0:
            gpa = total_points / total_credits
            
            st.success(f"**Your GPA is: {gpa:.2f}**")
            st.write(f"Total Grade Points: {total_points:.2f}")
            st.write(f"Total Credit Hours: {total_credits}")

            # Optional: Display a summary table
            st.subheader("Semester Summary")
            df = pd.DataFrame(courses)
            st.dataframe(df)
        else:
            st.error("Please enter valid credit hours.")

# --- CGPA Calculator Function (Multiple Semesters) ---
def cgpa_calculator():
    st.title("CGPA Calculator (Multiple Semesters)")
    st.write("Enter the GPA and total credit hours for each of your past semesters.")

    num_semesters = st.number_input("How many semesters to include?", min_value=1, value=2)

    semesters = []
    total_weighted_points = 0.0
    total_credits = 0.0

    # Create input fields for each semester
    for i in range(num_semesters):
        st.write(f"--- Semester {i+1} ---")
        col1, col2 = st.columns(2)

        with col1:
            # Input for semester GPA
            sem_gpa = st.number_input(
                f"Semester {i+1} GPA", 
                min_value=0.0, 
                max_value=4.0, 
                step=0.01, 
                value=3.5, 
                key=f"sem_gpa_{i}"
            )
        
        with col2:
            # Input for semester credit hours
            sem_credits = st.number_input(
                f"Semester {i+1} Total Credit Hours", 
                min_value=1, 
                value=15, 
                key=f"sem_credits_{i}"
            )
            
        # Store data
        semesters.append({'Semester': f"Semester {i+1}", 'GPA': sem_gpa, 'Credits': sem_credits})
        
        # CGPA calculation: (GPA1*Credits1 + GPA2*Credits2) / (Credits1 + Credits2)
        total_weighted_points += sem_gpa * sem_credits
        total_credits += sem_credits

    # Calculate CGPA
    if st.button("Calculate CGPA"):
        if total_credits > 0:
            cgpa = total_weighted_points / total_credits
            
            st.success(f"**Your CGPA is: {cgpa:.2f}**")
            st.write(f"Total Weighted Points: {total_weighted_points:.2f}")
            st.write(f"Total Credit Hours: {total_credits}")
            
            # Optional: Display a summary table
            st.subheader("Overall Summary")
            df = pd.DataFrame(semesters)
            st.dataframe(df)
        else:
            st.error("Please enter valid credit hours.")

# --- Main App ---
# Run the first calculator
gpa_calculator()

# Add a visual separator
st.divider()

# Run the second calculator
cgpa_calculator()
