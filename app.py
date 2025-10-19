import streamlit as st
import pandas as pd

# --- Grade Point Mapping (REMOVED) ---
# We no longer need the GRADE_POINTS dictionary

# --- GPA Calculator Function (Single Semester) ---
def gpa_calculator():
    st.title("GPA Calculator (Single Semester)")
    st.write("Enter your courses, credits, and the numeric grade points for this semester.")

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
            # CHANGED: Ask for numeric grade point directly
            grade_point = st.number_input(
                f"Course {i+1} Grade Point",
                min_value=0.0,
                max_value=4.0, # You can change this if your scale is different
                step=0.1,      # Allows 3.0, 3.1, 3.3, 3.6, etc.
                value=3.0,     # A default value
                key=f"grade_point_{i}"
            )
        
        # Add the raw inputs to our list
        course_inputs.append({'credits': credits, 'grade_point': grade_point})

    # Calculate GPA
    if st.button("Calculate GPA"):
        total_points = 0.0
        total_credits = 0.0
        courses_summary = []

        # Process the inputs only after the button is clicked
        for i, course in enumerate(course_inputs):
            credits = course['credits']
            grade_point = course['grade_point'] # Get the numeric grade point
            
            # Direct calculation: (Credits * Grade Point)
            points = grade_point * credits
            total_points += points
            total_credits += credits
            
            # Add to summary list
            courses_summary.append({
                'Course': f"Course {i+1}", 
                'Credits': credits, 
                'Grade Point': grade_point
            })

        if total_credits > 0:
            gpa = total_points / total_credits
            
            st.success(f"**Your GPA is: {gpa:.2f}**")
            st.write(f"Total Grade Points: {total_points:.2f}")
            st.write(f"Total Credit Hours: {total_credits}")

            st.subheader("Semester Summary")
            # Create DataFrame with the new column name
            df = pd.DataFrame(courses_summary, columns=['Course', 'Credits', 'Grade Point'])
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
