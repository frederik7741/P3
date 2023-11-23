import sys
import time

def count_reps(exercise_time):
    # Simulate the time taken to perform the exercise
    time.sleep(int(exercise_time))
    # Placeholder for the number of repetitions counted
    reps_count = 7
    return reps_count

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--time':
        print("Usage: python count_reps.py --time <exercise_time_in_seconds>")
        sys.exit(1)

    # The second command line argument is the exercise time
    exercise_time = sys.argv[2]
    reps = count_reps(exercise_time)
    # Print reps to stdout to capture in Flask
    print(reps)
