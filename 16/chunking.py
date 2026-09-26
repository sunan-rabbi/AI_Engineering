info = """
The Evolution and Fundamentals of Data Structures

A data structure is a specialized format for organizing, processing, retrieving, and storing data in a computer’s memory so that operations can be performed efficiently. Without well-designed data structures, modern software applications would crawl to a halt when handling massive streams of information. At its core, computer science relies on selecting the right structure to balance memory consumption against processing speed.

To understand data structures, we must first distinguish them from abstract data types (ADTs). An ADT defines a logical model—such as a list, stack, or queue—specifying *what* operations can be performed (like push, pop, or insert) without prescribing *how* those operations are implemented in code. Conversely, the actual data structure provides the concrete implementation, utilizing physical memory pointers, contiguous memory blocks, or dynamic node allocations.

Data structures are broadly categorized into two main types: linear and non-linear. Linear data structures arrange elements sequentially, meaning each element is connected to its previous and next successor. Classic examples include arrays, linked lists, stacks, and queues. In an array, elements are stored in contiguous memory locations, allowing lightning-fast O(1) access by index, but making insertions and deletions expensive because shifting elements is required. Linked lists solve the shift problem by using nodes that point to the next address in memory, trading away random access speed for dynamic memory flexibility.

Non-linear data structures, on the other hand, do not form a sequence. Instead, elements connect in hierarchical or interconnected networks. Trees—such as binary search trees, AVL trees, and heaps—organize data hierarchically, making them ideal for database indexing and searching algorithms. Graphs take this a step further by modeling complex relationships through nodes (vertices) and edges, forming the backbone of social network mapping, routing algorithms, and recommendation engines.

Ultimately, the choice of a data structure dictates the efficiency of algorithms that operate on them, measured via Big-O notation. Whether building a real-time chat application using queues or rendering a 3D video game world using spatial octrees, mastering data structures is the foundational skill that separates novice programmers from expert software engineers.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter # type: ignore

# 1. Fixed size chunking

fixed = CharacterTextSplitter(separator="", chunk_size=100, chunk_overlap=0)

step = 0
for chunk in fixed.split_text(info):
    print(f"Fixed chunk: {step+1}\n")
    print(chunk)
    print()
    print("-"*50)
    print()
    step += 1


# 2. Paragraph chunking

paragraph = CharacterTextSplitter(separator="\n\n", chunk_size=350, chunk_overlap=0)

step = 0
for chunk in paragraph.split_text(info):
    print(f"Paragraph chunk: {step+1}\n")
    print(chunk)
    print()
    print("-"*50)
    print()
    step += 1


# 3. Recursive chunking

recursive = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

step = 0
for chunk in recursive.split_text(info):
    print(f"Recursive chunk: {step+1}\n")
    print(chunk)
    print()
    print("-"*50)
    print()
    step += 1

