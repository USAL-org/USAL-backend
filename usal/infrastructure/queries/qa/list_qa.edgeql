SELECT QASection {
    id,
    question,
    answer,
}
FILTER .type = <QAType>$type