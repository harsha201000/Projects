import random

questions = [
    {
        "question": "Which data structure uses FIFO (First In First Out)?",
        "options": ["A) Stack", "B) Queue", "C) Tree", "D) Graph"],
        "answer": "B"
    },
    {
        "question": "What is the time complexity of binary search?",
        "options": ["A) O(n)", "B) O(log n)", "C) O(n log n)", "D) O(1)"],
        "answer": "B"
    },
    {
        "question": "Which algorithm is used to find the shortest path in a weighted graph?",
        "options": ["A) DFS", "B) BFS", "C) Dijkstra's Algorithm", "D) Kruskal's Algorithm"],
        "answer": "C"
    },
    {
        "question": "Which machine learning algorithm is used for classification?",
        "options": ["A) Linear Regression", "B) K-Means", "C) Decision Trees", "D) PCA"],
        "answer": "C"
    },
    {
        "question": "Which of the following is a supervised learning method?",
        "options": ["A) K-Means", "B) DBSCAN", "C) Linear Regression", "D) Apriori"],
        "answer": "C"
    },
    {
        "question": "What does a perceptron represent in neural networks?",
        "options": ["A) A single neuron", "B) A loss function", "C) A dataset", "D) A training algorithm"],
        "answer": "A"
    },
    {
        "question": "Which data structure is best for implementing recursion?",
        "options": ["A) Queue", "B) Stack", "C) Heap", "D) Hash Table"],
        "answer": "B"
    },
    {
        "question": "Which algorithm is used for clustering?",
        "options": ["A) K-Means", "B) SVM", "C) Random Forest", "D) Naive Bayes"],
        "answer": "A"
    },
    {
        "question": "Which AI technique allows systems to learn from experience?",
        "options": ["A) Hardcoding", "B) Machine Learning", "C) Rule-based systems", "D) Search algorithms"],
        "answer": "B"
    },
    {
        "question": "Which data structure is used in BFS?",
        "options": ["A) Stack", "B) Queue", "C) Priority Queue", "D) Hash Map"],
        "answer": "B"
    }
]

def play_quiz():
    print("\n🧠 Welcome to the Algorithms, Data Structures, ML & AI Quiz!")
    print("-------------------------------------------------------------")

    score = 0
    random.shuffle(questions)

    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for opt in q["options"]:
            print(opt)

        user_answer = input("Your answer (A/B/C/D): ").strip().upper()

        if user_answer == q["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer was {q['answer']}.")

    print("\n-------------------------------------------------------------")
    print(f"🎉 Quiz Complete! Your final score: {score}/{len(questions)}")
    print("-------------------------------------------------------------")

if __name__ == "__main__":
    play_quiz()