def insert_into_heap(heap, new_element):
    heap.append(new_element)
    index = len(heap) - 1  
    while index > 0:
        parent_index = (index - 1) // 2 
        if heap[parent_index] <= heap[index]: 
            break  
        heap[parent_index], heap[index] = heap[index], heap[parent_index]
        index = parent_index  
    return heap
heap=[10,12,15,16]
heap = insert_into_heap(heap, 17)
print("После добавления 17:", heap)