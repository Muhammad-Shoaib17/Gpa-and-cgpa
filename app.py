import streamlit as st
import pandas as pd

# --- Grade Point Mapping ---
# This dictionary is still used to look up the typed grade.
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
# We no longer need GRADE_OPTIONS

# --- GPA Calculator Function (Single Semester) ---
def gpa_calculator():
    st.title("GPA Calculator (Single Semester)")
    st.write("Enter your courses, credits, and grades for this semester.")

    num_courses = st.number_input("How many courses did you take?", min_value=1, value=4)

    # Store the user's inputs temporarily
    course_inputs = []

    for i in range(num_courses):
        st.write(f"--- Course {i+1} ---")
        col1, col2 = st.columns(2)
        
        with col1:
            credits = st.number_input(
                f"Course {i+1} Credit Hours", 
                min_value=1, 
                max_value=6, 
                value=3, 
                key=f"credits_{i}"
            )
        
        with col2:
            # CHANGED: Replaced st.selectbox with st.text_input
            grade_input = st.text_input(
                f"Course {i+1} Grade",
                placeholder="e.g., A, B+, C-",  # Guides the user
                key=f"grade_{i}"
            )
        
        # Add the raw inputs to our list
        course_inputs.append({'credits': credits, 'grade_input': grade_input})

    # Calculate GPA
    if st.button("Calculate GPA"):
        total_points = 0.0
        total_credits = 0.0
        courses_summary = []
        all_grades_valid = True # Flag to check inputs

        # Process the inputs only after the button is clicked
        for i, course in enumerate(course_inputs):
            credits = course['credits']
            grade_input = course['grade_input']
            
            # Standardize the input (uppercase, remove whitespace)
            grade = grade_input.upper().strip() 

            # Check if the typed grade is valid
            if grade in GRADE_POINTS:
                points = GRADE_POINTS[grade] * credits
                total_points += points
                total_credits += credits
                courses_summary.append({'Course': f"Course {i+1}", 'Credits': credits, 'Grade': grade})
            else:
                # If any grade is invalid, show an error and stop
                st.error(f"Invalid grade: '{grade_input}'. Please use a valid letter grade (e.g., A, A-, B+).", icon="❌")
                all_grades_valid = False
                break # Stop processing

        if all_grades_valid and total_credits > 0:
            gpa = total_points / total_credits
            
            st.success(f"**Your GPA is: {gpa:.2f}**")
            st.write(f"Total Grade Points: {total_points:.2f}")
            st.write(f"Total Credit Hours: {total_credits}")

            st.subheader("Semester Summary")
            df = pd.DataFrame(courses_summary)
            st.dataframe(df)
            
        elif all_grades_valid and total_credits == 0:
            st.error("Please enter valid credit hours.")
        # If all_grades_valid is False, the error message is already shown

# --- CGPA Calculator Function (Multiple Semesters) ---
def cgpa_calculator():
    st.title("CGPA Calculator (Multiple Semesters)")
    st.write("Enter the GPA and total credit hours for each of your past semesters.")

    num_semesters = st.number_input("How many semesters to include?", min_value=1, value=2)

    semesters = []
    total_weighted_points = 0.0
    total_credits = 0.0

    for i in range(num_semesters):
        st.write(f"--- Semester {i+1} ---")
        col1, col2 = st.columns(2)

        with col1:
            sem_gpa = st.number_input(
                f"Semester {i+1} GPA", 
                min_value=0.0, 
                max_value=4.0, 
                step=0.01, 
                value=3.5, 
                key=f"sem_gpa_{i}"
            )
        
        with col2:
            sem_credits = st.number_input(
                f"Semester {i+1} Total Credit Hours", 
                min_value=1, 
                value=15, 
                key=f"sem_credits_{i}"
            )
            
        semesters.append({'Semester': f"Semester {i+1}", 'GPA': sem_gpa, 'Credits': sem_credits})
        total_weighted_points += sem_gpa * sem_credits
        total_credits += sem_credits

    if st.button("Calculate CGPA"):
        if total_credits > 0:
            cgpa = total_weighted_points / total_credits
            
            st.success(f"**Your CGPA is: {cgpa:.2f}**")
            st.write(f"Total Weighted Points: {total_weighted_points:.2f}")
            st.write(f"Total Credit Hours: {total_credits}")
            
            st.subheader("Overall Summary")
            df = pd.DataFrame(semesters)
            st.dataframe(df)
        else:
            st.error("Please enter valid credit hours.")

# --- Main App ---
gpa_calculator()
st.divider()
cgpa_calculator()
