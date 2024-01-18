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

if length(ARGS) != 1
    println("usage: julia bpp_fomulation.jl <./file/path/file_name>")
    exit(1)
end

# Caminho relativo ao current work dir
num_items, basket_capacity, item_weight = read_file(ARGS[1])

num_bins = num_items

println("Quantidade de números: ", num_items)
println("Capacidade das cestas: ", basket_capacity)
println("Pesos: ", item_weight)

m = Model(GLPK.Optimizer;  add_bridges = false)

# var decisao: x[i, j] indica se o item i está na cesta j
@variable(m, x[1:num_items, 1:num_bins], Bin)
# indica se pelo menos um item foi atribuído na cesta j
@variable(m, y[1:num_items], Bin)

# 
@constraint(m,
            [i = 1:num_items, j = 1:num_bins],
            x[i,j] 
            <= y[j])

# Todos itens devem ser usados uma vez (soma das linhas)
@constraint(m, 
            [i = 1:num_items], 
            sum(x[i, j] for j in 1:num_bins)
            == 1)

# Limite de peso por cesta (soma das colunas)
@constraint(m, 
            [j = 1:num_bins],
            sum(item_weight[i] * x[i, j] for i in 1:num_items) 
            <= basket_capacity * y[j])

# Ocupar cestas de forma sequencial
@constraint(m,
            [j = 1:num_bins-1],
            y[j+1] 
            >= y[j])

@objective(m, Min, sum(y))
set_attribute(m, "tm_lim", 60 * 1_000)
optimize!(m)

# @show objective_value(m)
# @show JuMP.solve_time(m)
println("Número mínimo de cestos necessários: ", objective_value(m)) 
println("Tempo (s): ", JuMP.solve_time(m)) 

allocation = value.(x)

println("Id do item e peso em cada cesto:")
for j in 1:num_bins
    items_in_basket = findall(i -> allocation[i, j] > 0, 1:num_items)
    total_weight = isempty(items_in_basket) ? 0 : sum(item_weight[i] for i in items_in_basket)
    
    if (!isempty(items_in_basket)) 
        println("Cesto $j: Itens $items_in_basket, Peso total: $total_weight")
    end
end
