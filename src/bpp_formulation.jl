using JuMP
using GLPK

function read_file(file_name)
    # all numbers in file
    data = readlines(file_name)
    # fst line - number of itens
    num_items = parse(Int, data[1])
    # snd line - capacity of all baskets
    basket_capacity = parse(Int, data[2])
    # rest of the lines - weight of each item
    item_weight = [parse(Int, line) for line in data[3:end]]

    return num_items, basket_capacity, item_weight
end

# Caminho relativo ao current work dir
num_items, basket_capacity, item_weight = read_file("./selected_bpp_instances/teste.txt")

println("Quantidade de números: ", num_items)
println("Capacidade das cestas: ", basket_capacity)
println("Pesos: ", item_weight)

m = Model(GLPK.Optimizer)

# var decisao: x[i, j] indica se o item i está na cesta j
@variable(m, x[1:num_items, 1:num_items], Bin)
# indica se pelo menos um item foi atribuído na cesta j
@variable(m, y[1:num_items], Bin)

# Todos itens devem ser usados uma vez (soma das linhas)
for i in 1:num_items
    @constraint(m,
                sum(x[i, j] for j in 1:num_items)
                == 1)
end

# Limite de peso por cesta (soma das colunas)
for j in 1:num_items
    @constraint(m,
                sum(item_weight[i] * x[i, j] for i in 1:num_items)
                <= basket_capacity)
end

# Lista com cestas contendo pelo menos 1 item (se soma coluna >= 1 y = 1)
for j in 1:num_items
    @constraint(m,
                y[j] 
                == sum(x[i, j] for i in 1:num_items))
end

#@objective(m, Min, sum(y[j] for j in 1:num_items))
optimize!(m)

@show JuMP.value.(x)
@show JuMP.value.(y)
allocation = value.(x)

println("Id do item e peso em cada cesto:")
for j in 1:num_items
    items_in_basket = findall(i -> allocation[i, j] > 0, 1:num_items)
    total_weight = isempty(items_in_basket) ? 0 : sum(item_weight[i] for i in items_in_basket)
    
    if (!isempty(items_in_basket)) 
        println("Cesto $j: Itens $items_in_basket, Peso total: $total_weight")
    end

end

