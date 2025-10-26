class PIIData {
  index int
  dataType string
  value string
}

class PIIExtraction {
  privateData PIIData[]
  containsSensitivePII bool @description("E.g. SSN")
}




function ExtractPII(document: string) -> PIIExtraction {
  client "openai/gpt-5-mini"
  prompt #"
    Extract all personally identifiable information (PII) from the given document. Look for items like:
    - Names
    - Email addresses
    - Phone numbers
    - Addresses
    - Social security numbers
    - Dates of birth
    - Any other personal data

    {{ ctx.output_format }}

    {{ _.role("user") }} 
    
    {{ document }}
  "#
}

test BasicPIIExtraction {
  functions [ExtractPII]
  args {
    document #"
      John Doe was born on 01/02/1980. 
      His email is john.doe@email.com and phone is 555-123-4567.
      He lives at 123 Main St, Springfield, IL 62704.
    "#
  }
}

test EmptyDocument {
  functions [ExtractPII]
  args {
    document "This document contains no PII data."
  }
}
