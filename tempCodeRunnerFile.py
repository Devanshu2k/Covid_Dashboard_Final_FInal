fig = plt.figure(figsize=(20, 12))
plt.bar(top_10_mortality_rate['Country/Region'], top_10_mortality_rate['mortality_rate'])
plt.title("TOP 10 COUNTRIES WITH THE HIGHEST MORTALITY RATES\n",
        size=15,color='#28a9ff')
plt.xticks(rotation = 90)
plt.ylabel('MORTALITY RATE')
plt.xlabel('COUNTRY')
plt.show()