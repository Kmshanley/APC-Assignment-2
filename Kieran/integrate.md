# Integration Method

## Requirements
- Most requirements are given from assignment brief
- Make assumptions for gaps in given requirements

## Component analysis
- [OpenEduCat](https://openeducat.org/)
    - Open source software, easy to modify to fit requirements
    - Easy to audit for security and speed
- [ofCourse](https://www.ofcourse.org/)
    - Closed source software, very difficult to modify
    - If you're a big enough customer it may be possible to get custom features 
    - Closed source is hard to audit for security

## Requirement modifications
- If using a open source software, assess if modifications are possible
- If using closed source software, work with provider and assess if modifications/customizations are possible
- Either compromise on requirements or return to component analysis to meet all requirements

## System design (with reuse)
- Implement chosen system
     - May be implemented in house or with the assistance of contracted engineers
- If modifying existing system use Incremental, Waterfall or other methodology to manage progress of modifications

## Development and integration
- Deployment of system
    - Deploy small test system in-house first
- Acquire hardware or cloud resources to support large scale  

## System Validation
- Conduct small scale tests <100 users 
- Conduct large scale tests > 1000 users 
- Can be staged rollout or straight transition