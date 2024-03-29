#include "SingleAgentSolver.h"


list<Node> SingleAgentSolver::getNextLocations(Node curr) const // including itself and its neighbors
{
	list<Node> rst = instance.getNeighbors(curr);
	rst.emplace_back(curr);
	return rst;
}


void SingleAgentSolver::compute_heuristics()
{

	my_heuristic.resize(instance.map_size, MAX_TIMESTEP);

	// generate a heap that can save nodes (and a open_handle)
	boost::heap::pairing_heap< Node, boost::heap::compare<Node::compare_node> > heap;

	Node root(goal_location, 0);
	my_heuristic[goal_location] = 0;
	heap.push(root);  // add root to heap
	while (!heap.empty())
	{
		Node curr = heap.top();
		heap.pop();
		for (int next_location : instance.getNeighbors(curr.location))
		{
			if (my_heuristic[next_location] > curr.value + 1)
			{
				my_heuristic[next_location] = curr.value + 1;
				Node next(next_location, curr.value + 1);
				heap.push(next);
			}
		}
	}
}