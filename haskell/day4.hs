import Data.Char
import Data.Maybe

hello :: Char -> Int
hello a = (digitToInt a)

isSixDigit :: Int -> Bool
isSixDigit i = ((length (show i) == 6) && (head (show i) /= '0'))

adjacentSame :: Int -> Bool
adjacentSame i = adj (show i) where
    adj :: String -> Bool
    adj [] = False
    adj (x:[]) = False
    adj (x:xs) = if (x == (head xs))
                    then True
                    else adj xs

notDecreasing :: Int -> Bool
notDecreasing i = nDec (show i) where
    nDec :: String -> Bool
    nDec [] = True
    nDec (x:[]) = True
    nDec (x:xs) = if (digitToInt x) > (digitToInt $ head xs)
                    then False
                    else nDec xs

groupConsecutive :: (Eq a) => [a] -> [[a]]
groupConsecutive [] = []
groupConsecutive (x:[]) = [[x]]
groupConsecutive (x:xs) = gcs [] (x:xs) where
    gcs :: (Eq a) => [[a]] -> [a] -> [[a]]
    gcs c [] = c
    gcs [] (x:xs) = gcs [[x]] xs
    gcs c (x:xs) = if x == (head $ last c)
                    then gcs ((init c) ++ [([x] ++ last c)]) xs
                    else gcs (c ++ [[x]]) xs

checkEvenGroups :: [[a]] -> Bool
checkEvenGroups [] = True
checkEvenGroups xs = foldr (||) False (map check xs) where
    check :: [a] -> Bool
    check [] = False
    check (x:[]) = False
    check xs = length xs == 2

adjacentSamePairs :: Int -> Bool
adjacentSamePairs i = adj (show i) where
    adj :: String -> Bool
    adj xs = checkEvenGroups $ groupConsecutive xs

part1Test :: Int -> Bool
part1Test a = isSixDigit a && adjacentSame a && notDecreasing a

part2Test :: Int -> Bool
part2Test a = isSixDigit a && adjacentSamePairs a && notDecreasing a

meetCriteria :: Int -> Int -> Int
meetCriteria s e = length [a | a <- [s..e], part1Test a]

meetCriteriaPart2 :: Int -> Int -> Int
meetCriteriaPart2 s e = length [a | a <- [s..e], part2Test a]
