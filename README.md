# Book's Recommender System using Content-based and CF-based Algorithm

A recommender system is a subclass of information filtering system that seeks to predict the rating or preference a user would give to an item. In this project, I try to build a simple recommender system for books on <a href="https://www.goodreads.com" target="_blank">Goodreads</a>. Goodreads is one of the largest site for readers and book recommendations.

<br>
Book's data used in this project can be obtained <a href="https://www.github.com/zygmuntz/goodbooks-10k" target="_blank">here</a>. The original data consist of 5,976,479 ratings which are given by 53,424 users for 10,000 books. For this project, I only use subset of the original data due to limitation of hardware and to prevent MemoryError during data processing. So for the recommender system, the final data consist of 361,156 ratings which are given by 4,011 users for 762 books. The completed dashboard can be found <a href="https://recommender-system-goodreads.herokuapp.com/" target="_blank">here</a>


<br>I use two approaches to build the book's recommender system:
* **Content-based Recommendation** <br>
  This approach gives recommendation only based on features of the item itself. In this project, I use three features of each book which are **Title**, **Author**, and **Tag** to give book's recommendations.
* **Collaborative Filtering (CF)-based Recommendation** <br>
  This approach gives recommendation based on historical preference of a user or ratings of other items (hence the name 'collaborative'). For this approach, I try two of the most common algorithms such as user-based CF and item-based CF. For these methods, I try the standard one and the other method that taking into account the mean ratings of each user.<br><br>
  I also try other methods including Matrix Factorization (Singular Value Decomposition / SVD), Slope One, and Co-clustering. SVD is an advanced method to overcome limitation of CF-based Recommendation such as sparsity, scalability, and cold start. Slope One is another simpler yet accurate approach to item-based CF. Co-clustering is based on fuzzy clustering where users and items are assigned to clusters and co-clusters.<br><br>
  In this project, the chosen algorithm is item-based CF with means since it gives the smaller error (RMSE) compared to other algorithms.
