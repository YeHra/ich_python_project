import logwriter_gem
import logreader
import db_gem



db_conn = db.connection()

result = db.result
logwriter.search_log()
def paginator():
    start = 0
    end = 10
    while True:
        output = result[start:end]
        if not output:
            break
        elif len(output) < 10:
            print(*output, sep = '\n')
            break
        print(*output, sep = '\n')
        start += 10
        end += 10
        ask = input('Вывести следующие 10 результатов? Yes/No').lower()
        if ask =='yes':
            print(*output[start:end], sep='\n')
        else:
            break
res = logwriter.five_latest_query()
print(*res, sep = '\n')
res1 = (logwriter.five_popular_query())
print(*res1, sep = '\n')
