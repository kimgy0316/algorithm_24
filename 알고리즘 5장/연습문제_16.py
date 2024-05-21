class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def count_nodes(root):
    if root is None:
        return 0
    else:
        left_count = count_nodes(root.left)
        right_count = count_nodes(root.right)
        return 1 + left_count + right_count

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

node_count = count_nodes(root)
print("이진 트리의 노드 수:", node_count)
