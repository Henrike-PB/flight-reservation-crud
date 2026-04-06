"""
Desafio de Lógica 1

Dado um array de números inteiros e um alvo (target), encontre os índices de dois 
números que somam esse alvo.
Você não pode reutilizar o mesmo elemento, e sempre existe uma solução.

Exemplo:

Entrada:
nums = [2, 7, 11, 15], target = 9

Saída:
[0, 1]

Porque: 
2 + 7 = 9
"""


def two_sum(nums, target):
    vistos = {} 
    
    for i in range(len(nums)):
        num = nums[i]
        complemento = target - num

        if complemento in vistos:
            return [vistos[complemento], i]

        vistos[num] = i
        
    return []

'''
Aqui iremos implementar a função two_sum que recebe uma lista de números (nums) e um número alvo (target).
A função utiliza um dicionário (vistos) para armazenar os números já vistos e seus índices correspondentes.
'''

if __name__ == "__main__":
    print("--- Iniciando teste de validação ---\n")

  
    nums1, target1 = [2, 7, 11, 15], 9
    resultado1 = two_sum(nums1, target1)
    print(f"Teste 1: nums={nums1}, target={target1}")
    print(f"Resultado: {resultado1} (Esperado: [0, 1])\n")