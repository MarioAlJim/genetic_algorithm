def classify_triangle(a, b, c):
    # Verificar si los lados forman un triángulo válido
    if a <= 0 or b <= 0 or c <= 0:
        return "not a triangle"

    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            return "equilateral"
        elif a == b or a == c or b == c:
            return "isosceles"
        else:
            return "scalene"
    else:
        return "not a triangle"