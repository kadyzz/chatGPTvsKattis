from autokattis import Kattis

# Initialize Kattis instance
kattis_instance = Kattis("kadriye-yildiz", "@UY7hbbCwQYv@x3")

print(kattis_instance.problems(*[True]*4).to_df())      