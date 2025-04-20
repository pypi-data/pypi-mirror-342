function fizzBuzz(n) {
for (let i = 1; i <= n; i++) {
if (i % 3 === 0 && i % 5 === 0) {
console.log("FizzBuzz");
} else if (i % 3 === 0) {
console.log("Fizz");
} else if (i % 5 === 0) {
console.log("Buzz");
} else {
console.log(i);
}
}
}

// Example usage:
fizzBuzz(100);

// Example usage: different range
fizzBuzz(25);

// Example one-line output. (arrow function & ternary operator)
const fizzBuzzOneLine = n => {
for (let i = 1; i <= n; i++) {
console.log((i % 3 === 0 ? (i % 5 === 0 ? "FizzBuzz" : "Fizz") : (i % 5 === 0 ? "Buzz" : i)));
}
};
fizzBuzzOneLine(30);
