from matplotlib import pyplot as plt
import pandas as pd

# manually replace &amp; with and

# Loading Data
book_ratings = pd.read_csv("data/BX-Book-Ratings.csv", sep=';')
books = pd.read_csv("data/BX-Books.csv", sep=";") 
users = pd.read_csv("data/BX-Users.csv", sep=";")

# Data Inspection 
print ( users.shape, users.head(), users.info() )
print ( books.shape, books.head(), books.info() )
print ( book_ratings.shape, book_ratings.head(), book_ratings.info() )

# inspect possible predictors further


plt.rc("font", size=15)
users.BookRating.value_counts(sort=False).plot(kind='bar')
plt.title('Distribution\n')
plt.xlabel('BookRating')
plt.ylabel('Count')
plt.show()
