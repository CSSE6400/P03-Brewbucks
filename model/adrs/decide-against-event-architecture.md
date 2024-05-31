##### Decide Against Changing to Event Driven Architecture
**Date:** 2024-05-05  
**Status:** Accepted  
#### Summary
In the context of delivering a simple, coffee ordering website, with tight time constraints, we decided to stay with our original plan for a service-based architecture. We believe this decision best balances our objectives and time. Any additional time leftover can be spent further supporting the QAs.

#### Context
* Brewbucks quality attributes are better supported by event-driven architecture: scalability, reliability, interoperability, modularity
* Event-driven architecture is more complex to implement, e.g, need to add queue, learn libraries to implement event broker and/or a DSL we've not familar with
* Service based architecture can be improved to support the QAs (i.e., multiple instances for availability (and somewhat scalability), stateless service pattern for reliability)
* Development team prefers to not implement a queue
* Brief recommends a service-based architecture
* Time constraints make it difficult to change architecture unless there's significant advantages

#### Decision
An event-driven architecture will not be followed for Brewbucks. Instead, a service-based architecture will be pursued. 

#### Consequences
###### Advantages  
* Simpler to implement service-based architecture  
* Avoids complications of working with queues, new libraries in event-driven architecture

###### Disadvantages  
* Should add extensions to service-based architecture to better support QAs

