import java.util.HashSet;
import java.util.Set;

/**
 * BinomialHeap
 *
 * An implementation of binomial heap over non-negative integers. Based on
 * exercise from previous semester.
 */
public class BinomialHeap {
	public int size;
	public HeapNode last;
	public HeapNode min;
	int linksCounter = 0;
	int deletedNodesDegreesSum = 0;

	// constructors
	public BinomialHeap() {
	};

	public BinomialHeap(int size, BinomialHeap.HeapNode last, BinomialHeap.HeapNode min) {
		super();
		this.size = size;
		this.last = last;
		this.min = min;
	}

	/**
	 * @pre x != Null and y != Null
	 * @pre x.next == x && y.next == y
	 * 
	 * @param x: heapNode that is a root of some k degree binomial tree
	 * @param y: heapNode that is a root of another k degree binomial tree
	 *
	 * @return new k+1 degree binomial tree
	 */
	public HeapNode link(HeapNode x, HeapNode y) {
		if (x.getKey() > y.getKey()) {
			HeapNode temp = x;
			x = y;
			y = temp;
		}
		x.setChild(y);
		return x;
	}

	/**
	 *
	 * returns the degree of the biggest tree in this binomial heap
	 *
	 */
	public int getMaxDegree() {
		return this.last.rank;
	}

	/**
	 *
	 * pre: key > 0
	 *
	 * Insert (key,info) into the heap and return the newly generated HeapItem.
	 *
	 */
	public HeapItem insert(int key, String info) {
		HeapItem item = new HeapItem(null, key, info);
		HeapNode node = new HeapNode(item, null, null, null, 0);
		node.next = node;
		item.node = node;
		BinomialHeap binHeap = new BinomialHeap(1, node, node);
		this.meld(binHeap);
		return item;
	}

	/**
	 *
	 * Delete the minimal item
	 *
	 */
	public void deleteMin() {
		if (this.empty()) {
			return;
		}

		// if min is the only evar //
		deletedNodesDegreesSum += this.min.rank;
		if (this.recalculateSize() == 1) {
			last = null;
			min = null;
			this.size = 0;
			return;
		}

		HeapNode childOfMin = min.child;

		HeapNode min = this.min;

		// -----delete the minimum physically-----

		if (this.numTrees() == 1) {
			this.last = null;
			this.min = null;
			this.size = 0;
			min.child = null;
		} else {
			HeapNode prev = min;
			while (prev.next != min) {
				prev = prev.next;
			}
			prev.next = min.next;
			min.next = min;
			min.child = null;
			if (this.last == this.min) {
				this.last = prev;
			}
		}

		// -- if min.rank ==0 -- (min doesnt have children) //
		if (min.rank == 0) {

			// - update min field - //
			min.next = min;
			this.size -= 1;
			SearchForMin();
			return;
		}

		// -----get the new trees (the childs of deleted minimum)-----

		BinomialHeap newBinHeap = new BinomialHeap();
		newBinHeap.last = childOfMin;
		int r = childOfMin.rank;
		for (int i = 0; i <= r; i++) {
			childOfMin.parent = null;
			childOfMin = childOfMin.next;
		}
		newBinHeap.min = newBinHeap.SearchForMin().node;
		newBinHeap.size = newBinHeap.recalculateSize();
		// -----meld this with newBinHeap-----
		this.meld(newBinHeap);

		// -- update field min -- //
		SearchForMin();
	}

	/**
	 *
	 * Return the minimal HeapItem
	 * 
	 * @pre this.min.key <= node.min.key for each node in this
	 * 
	 * @implNote: this function costs O(1)
	 *
	 */
	public HeapItem findMin() {
		if (this.last == null) {
			return null;
		}
		return this.min.item;
	}

	/**
	 * Update the minimal HeapItem Return the minimal HeapItem
	 *
	 * @implNote: this function may cost O(log n) because it searches the minimum in
	 *            naiive way
	 *
	 */
	public HeapItem SearchForMin() {

		if (this.last == null) {
			return null;
		}
		HeapNode min = this.last;
		HeapNode curr = this.last;
		do {
			if (curr.item.key < min.item.key) {
				min = curr;
			}
			curr = curr.next;
		} while (curr != last);

		this.min = min;
		return min.item;

		/**
		 * HeapNode last_node = this.last; HeapNode curr_node = last_node.next; HeapNode
		 * min_node = curr_node; int min = -10; while(curr_node != last_node){ if
		 * (curr_node.item.key > min){ min_node = curr_node; min = curr_node.item.key; }
		 * curr_node = curr_node.getNext(); } this.min = min_node; return min_node.item;
		 **/
	}

	/**
	 * pre: item.node != null pre: 0<diff<item.key
	 *
	 * Decrease the key of item by diff and fix the heap.
	 *
	 */
	public void decreaseKey(HeapItem item, int diff) {
		// -----decrease-----
		item.key = item.key - diff;

		// -----fix the heap-----
		HeapNode parent = item.node.parent;
		if (parent == null) {
			// --update field min and return --//
			if (item.key < min.getKey()) {
				min = item.node;
			}
			return;
		}
		while (parent != null) {
			HeapItem parentItem = parent.item;
			if (parentItem.key > item.key) {
				parentItem.swapNodes(item);
			} else {
				break;
			}
			parent = parent.parent;
		}

		/// - update filed min --//
		if (item.key < min.item.key) {
			min = item.node;
		}

	}

	/**
	 *
	 * Delete the item from the heap.
	 *
	 */
	public void delete(HeapItem item) {
		decreaseKey(item, item.key + 1);
		deleteMin();
		return;
	}

	/**
	 *
	 * Meld the heap with heap2
	 *
	 */
	public void meld(BinomialHeap heap2) {
		// special cases: one of the heaps or both is empty
		if (heap2.empty()) {
			return;
		} else if (this.empty()) {
			this.last = heap2.last;
			this.size = heap2.size;
			this.min = heap2.min;
			return;
		}

		// (this) and (heap2) are not empty:
		//HeapNode newMin = (this.min.getKey() < heap2.min.getKey()) ? this.min : heap2.min;
		int newLen = Math.max(this.getMaxDegree(), heap2.getMaxDegree()) + 2;
		HeapNode[] thisArr = new HeapNode[newLen];
		HeapNode[] heap2Arr = new HeapNode[newLen];
		HeapNode[] result = new HeapNode[newLen];

		HeapNode curr = this.last;
		do {
			thisArr[curr.rank] = curr;
			curr = curr.next;
		} while (curr != this.last);
		curr = heap2.last;
		do {
			heap2Arr[curr.rank] = curr;
			curr = curr.next;
		} while (curr != heap2.last);

		// -----Binary addition-----
		for (int i = 0; i < result.length - 1; i++) {
			HeapNode t1 = thisArr[i];
			HeapNode t2 = heap2Arr[i];

			if (t1 != null) {
				t1.next = t1;
			}
			if (t2 != null) {
				t2.next = t2;
			}

			if (result[i] != null) {// carry == true
				if (t1 != null && t2 != null) {
					result[i + 1] = link(t1, t2);
					linksCounter++;
				} else if (t1 != null && t2 == null) {
					result[i + 1] = link(t1, result[i]);
					linksCounter++;
					result[i] = null;
				} else if (t1 == null && t2 != null) {
					result[i + 1] = link(result[i], t2);
					linksCounter++;
					result[i] = null;
				}
			} else {// curry == false
				if (t1 != null && t2 != null) {
					result[i + 1] = link(t1, t2);
					linksCounter++;
				} else if (t1 != null && t2 == null) {
					result[i] = t1;
				} else if (t1 == null && t2 != null) {
					result[i] = t2;
				}
			}
		}

		// -----build bionomialHeap from result-----
		this.last = null;
		HeapNode smallestTree = null;
		HeapNode biggestTree = null;
		int i = 0;
		while (i < result.length) {
			if (result[i] != null) {
				if (smallestTree == null) {
					smallestTree = result[i];
					biggestTree = result[i];
				}
				int j = i + 1;
				while (j < result.length) {
					if (result[j] == null) {
						j++;
					} else {
						break;
					}
				}
				if (j < result.length) {// means that result[j] != null
					biggestTree = result[j];
					result[i].next = result[j];
					i = j;
				} else {
					result[i].next = smallestTree;
					break;
				}
			} else {
				i += 1;
			}
		}
		this.last = biggestTree;
		this.min = this.SearchForMin().node;
		this.size = this.recalculateSize();
	}

	/**
	 *
	 * Return the number of elements in the heap
	 *
	 * @implNote: this function costs O(1)
	 */
	public int size() {
		return this.size;
	}

	/**
	 *
	 * Return the number of elements in the heap
	 *
	 * @implNote: this function may cost O(log n) because it recalculates the size
	 *            by summing the size of each tree
	 */
	public int recalculateSize() {
		if (this.empty()) {
			return 0;
		}
		HeapNode node = this.last;
		HeapNode curr = node.next;
		int size_tree = (int) Math.pow(2, node.rank);
		while (curr != node) {
			size_tree += Math.pow(2, curr.rank);
			curr = curr.next;
		}
		return size_tree;
	}

	/**
	 *
	 * The method returns true if and only if the heap is empty.
	 *
	 */
	public boolean empty() {
		return last == null;
	}

	/**
	 *
	 * Return the number of trees in the heap.
	 *
	 */
	public int numTrees() {
		if (this.recalculateSize() == 0) {
			return 0;
		}
		int cnt = 1;
		HeapNode node = this.last;
		HeapNode next = node.next;
		while (next != node) {
			cnt++;
			next = next.next;
		}
		return cnt;
	}

	/**
	 * Class implementing a node in a Binomial Heap.
	 *
	 */
	public class HeapNode {
		public HeapItem item;
		public HeapNode child;
		public HeapNode next;
		public HeapNode parent;
		public int rank;

		public HeapNode(HeapItem item, HeapNode child, HeapNode next, HeapNode parent, int rank) {
			this.child = child;
			this.item = item;
			this.next = next;
			this.parent = parent;
			this.rank = rank;
		}

		// ------------Sets------------//

		/**
		 * @param child != Null
		 * @pre: pre(child).rank <= post(child).rank
		 *
		 * @post: post(rank) = pre(rank) + 1
		 *
		 * @apiNote: the old parent of the new child may still think that child is his
		 *           child
		 **/
		public void setChild(HeapNode child) {
			HeapNode temp = this.child;
			this.child = child;
			child.parent = this;
			if (temp != null) {
				child.next = temp.next;
				temp.next = child;
			}

			this.rank++;
		}

		public int getKey() {
			return this.item.key;
		}

		public String getInfo() {
			return this.item.info;
		}
	}

	/**
	 * Class implementing an item in a Binomial Heap.
	 *
	 */
	public class HeapItem {
		public HeapNode node;
		public int key;
		public String info;

		/**
		 *
		 * @param node
		 * @param key
		 * @param info
		 */
		public HeapItem(HeapNode node, int key, String info) {
			this.node = node;
			this.key = key;
			this.info = info;
		}

		/**
		 *
		 * swaps the node's items
		 *
		 * @pre OtherItem != null
		 * @pre this.node != null && otherItem.node != null
		 * @param Otheritem
		 *
		 * @post items swapped
		 */
		public void swapNodes(BinomialHeap.HeapItem Otheritem) {
			HeapNode temp = this.node;
			this.node = Otheritem.node;
			Otheritem.node = temp;

			this.node.item = this;
			Otheritem.node.item = Otheritem;
		}

	}

	public void print() {
		System.out.println("Binomial Heap:");
		System.out.println("Size: " + size);

		if (min != null) {
			System.out.println("Minimum Node: " + min.item.key);
		} else {
			System.out.println("No minimum node.");
		}

		System.out.println("Heap Nodes:");
		if (last != null) {
			Set<HeapNode> visited = new HashSet<>();
			printHeapNode(last, 0, visited);
		} else {
			System.out.println("No heap nodes.");
		}
	}

	private void printHeapNode(HeapNode node, int indentLevel, Set<HeapNode> visited) {
		StringBuilder indent = new StringBuilder();
		for (int i = 0; i < indentLevel; i++) {
			indent.append("    ");
		}

		System.out.println(indent + "Key: " + node.item.key);
		System.out.println(indent + "Info: " + node.item.info);
		System.out.println(indent + "Rank: " + node.rank);

		visited.add(node);

		if (node.child != null && !visited.contains(node.child)) {
			System.out.println(indent + "Child:");
			printHeapNode(node.child, indentLevel + 1, visited);
		}

		if (node.next != null && !visited.contains(node.next)) {
			System.out.println(indent + "Sibling:");
			printHeapNode(node.next, indentLevel, visited);
		}
	}

}