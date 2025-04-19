class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val        
        self.next = next       
def delete_node_at_index(head, index):
    if index < 0:
        return head
    if index == 0:
        return head.next  
    current = head
    for i in range(index - 1):
        if not current or not current.next:
            return head  
        current = current.next
    if current.next:
        current.next = current.next.next
    return head
node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node1.next = node2
node2.next = node3
index = int(input("Введите индекс элемента для удаления: "))
new_head = delete_node_at_index(node1, index)
current = new_head
while current:
    print(current.val, end=" -> ")
    current = current.next
print("")