from testpe import brute_force

from commons import from_csv_to_list_of_dict

shares = from_csv_to_list_of_dict('data/dataset1_Python+P7.csv')
brute_force(

    dataset=shares,
    force=10,
    accept=lambda x: x["cost"] < 500,
    evaluate=lambda x, y: x["gains"] > y["gains"],
    combine=lambda dataset, x: {
       "combination": x,
       "cost": sum([dataset[i]["cost"] for i in x]),
       "gains": sum([dataset[i]["gains"] for i in x])
    },
    serialize=lambda x: f"{','.join([str(x) for x in x['combination']])}:{x['cost']}:{x['gains']}",
    deserialize=lambda x: {
        'combination': x.split(":")[0].split(","),
        'cost': float(x.split(":")[1]),
        'gains': float(x.split(":")[2])
    },
    best_match_file_path="best_match.txt"
)