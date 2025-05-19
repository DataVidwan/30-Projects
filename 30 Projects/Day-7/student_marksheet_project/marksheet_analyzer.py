import pandas as pd

# Step 1: Load CSV data
df = pd.read_csv("marks.csv")

print("\n🎓 Full Marksheet:")
print(df.to_string(index=False))

# Step 2: Calculate Total and Average marks for each student
df["Total"] = df.iloc[:, 1:].sum(axis=1)
df["Average"] = df.iloc[:, 1:-1].mean(axis=1).round(2)

# Step 3: Determine Pass/Fail (Pass if all subjects >= 35)
df["Status"] = df.iloc[:, 1:5].apply(lambda x: "Pass" if (x >= 35).all() else "Fail", axis=1)

print("\n📊 Marksheet with Total, Average and Status:")
print(df.to_string(index=False))

# Step 4: Top Performer
top_score = df["Total"].max()
top_students = df[df["Total"] == top_score]["Name"].values
print(f"\n🏅 Top Performer(s): {', '.join(top_students)} with {top_score} marks")

# Step 5: Subject-wise average
subject_averages = df.iloc[:, 1:5].mean()
print("\n📈 Subject-wise Average Marks:")
for subject, avg in subject_averages.items():
    print(f"{subject}: {avg:.2f}")

# Step 6: List failed students
failed = df[df["Status"] == "Fail"]
if not failed.empty:
    print("\n❌ Students who failed in at least one subject:")
    print(failed[["Name", "Status"]].to_string(index=False))
else:
    print("\n✅ All students passed!")

# Optional: Export result
df.to_csv("final_result.csv", index=False)
print("\n💾 Final results saved to 'final_result.csv'")
