using JuMP
using GLPK

function read_file(file_name)
    # all numbers in file
    data = readlines(file_name)
    # fst line - number of itens
    num_items = parse(Int, data[1])
    # snd line - capacity of all baskets
    bin_capacity = parse(Int, data[2])
    # rest of the lines - weight of each item
    weights = [parse(Int, line) for line in data[3:end]]

    return num_items, bin_capacity, weights
end

if length(ARGS) == 1
    file_path = ARGS[1]
    timeout = 1
elseif length(ARGS) == 2
    file_path = ARGS[1]
    timeout   = parse(Float64, ARGS[2])
else
    println("usage: julia bpp_fomulation.jl <./file/path/file_name> <timeout (hours)>")
    exit(1)
end

# Caminho relativo ao current work dir
num_items, bin_capacity, weights = read_file(file_path)

# Estimativa de bins
# Pega os itens e coloca em uma bin que ainda tem espaco (primeiro que couber)
assignment = [[]]
for i in 1:num_items
    item_weight = weights[i]
    placed = false

    if size(assignment[1],1) == 0
        push!(assignment[1], i)
        continue
    end

    for bin in assignment
        if sum(weights[x] for x in bin) + item_weight <= bin_capacity 
            push!(bin, i)
            placed = true
            break
        end
    end

    if !placed
        push!(assignment, [i])
    end
end
max_bins = size(assignment,1)

println("---------------------------------------------------------------")
println("Estimativa: ", max_bins)
println("Quantidade de números: ", num_items)
println("Capacidade das cestas: ", bin_capacity)
println("Pesos: ", weights)

m = Model(GLPK.Optimizer;  add_bridges = false)
set_attribute(m, "tm_lim", 3600 * timeout * 1_000)

# var decisao: x[i, j] indica se o item i está na cesta j
@variable(m, x[1:num_items, 1:max_bins], Bin)
# indica se pelo menos um item foi atribuído na cesta j
@variable(m, y[1:num_items], Bin)

# 
@constraint(m,
            [i = 1:num_items, j = 1:max_bins],
            x[i,j] 
            <= y[j])

# Todos itens devem ser usados uma vez (soma das linhas)
@constraint(m, 
            [i = 1:num_items], 
            sum(x[i, j] for j in 1:max_bins)
            == 1)

# Limite de peso por cesta (soma das colunas)
@constraint(m, 
            [j = 1:max_bins],
            sum(weights[i] * x[i, j] for i in 1:num_items) 
            <= bin_capacity * y[j])

# Ocupar cestas de forma sequencial
@constraint(m,
            [j = 2:max_bins],
            y[j-1] 
            >= y[j])

@objective(m, Min, sum(y))
optimize!(m)

println()
println("Número mínimo de cestos necessários: ", objective_value(m)) 
println("Tempo (s): ", JuMP.solve_time(m)) 

allocation = value.(x)

println("Id do item e peso em cada cesto:")
for j in 1:max_bins
    items_in_basket = findall(i -> allocation[i, j] > 0, 1:num_items)
    total_weight = isempty(items_in_basket) ? 0 : sum(weights[i] for i in items_in_basket)
    
    if (!isempty(items_in_basket)) 
        println("Cesto $j: Itens $items_in_basket, Peso total: $total_weight")
    end
end
