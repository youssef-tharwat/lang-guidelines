# agency

Structure long-running, concurrent parts of a system as agents that own their resources and cleanup, since JavaScript has no destructors.

**Sources:** P:systemic-4-agency, P:complication-6-no-destructor

---

## Systemic 4 Agency (P:systemic-4-agency)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/systemic-4-agency), copyright the author, redistributed with attribution.

Approaching system design with agency in mind is crucial. Agency is the various aspects of an agent, something that works on behalf of the other. In the computer program context, an agent works on behalf of the user.

An agent within a program is usually a long-running and concurrent process that has a part (or sometimes the whole) of the user's purpose.

While crucial, agency cannot be explained clearly because there is no single implementation that can fulfill all its aspects.

*   [Modern OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) (as opposed to [Alan Kay's OOP](https://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented)) tried to imply and activeness of an object by enabling [methods](https://en.wikipedia.org/wiki/Method_(computer_programming)).
*   [Multithreading](https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)) tried to allow two sub-programs to run concurrently, allowing programmers to assume an active role within a system of several active roles. Messaging between agents would later take the form of [Mutex](https://en.wikipedia.org/wiki/Mutual_exclusion), [Channels](https://en.wikipedia.org/wiki/Channel_(programming)), [Semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)), etc.
*   [Agent-oriented programming](https://en.wikipedia.org/wiki/Agent-oriented_programming) essentially is a pattern to capture and synthesize the aspects of agents and agency.
*   Beliefs (e.g. over the meaning of signals, environment), capabilities, commitments, and message passing are partially fulfilled by the likes of interface, [typings](https://en.wikipedia.org/wiki/Datatyp), [serialization/deserialization](https://en.wikipedia.org/wiki/Serialization), etc, network.

A more concretely refined definition of agent I prefer is the independent multithreading-enabled self-centered code style combined with its outer shell interface definition reinforced with static typing, which looks like:

```
// pseudocode
thread.spawn(() => {
  // I'll do my own stuff here
  // regardless of my parent's state
});
```

### Merits of Previous Tips

If you have not visited the previous three articles, I suggest doing so:

*   [The Throwless Pact](https://valand.dev/systemic-ts/systemic-1-known-vs-unknown-error-throwless)
*   [Closure Over Class](https://valand.dev/systemic-ts/systemic-2-closure-over-class)
*   [Runtime Type Validation](https://valand.dev/systemic-ts/systemic-3-runtime-type-validation)

The merits of the three previous articles, the complication articles, and possibly the next articles culminate here. In building systems, the concept of agents eventually arises to combat the growing scale of the purpose of a system.

An agent, or more specifically the maintainer of a program-agent, the programmer, can only fit a number of symbols in one's memory at a time (i.e. name and meaning of types, functions, modules, routines, development processes, etc). One has to wrap a part of the purpose of the whole program into an agent, a sub-process that enacts tasks without direct supervision, and either report back or be examined at a lower intensity and frequency.

"Too complex" is a common complaint indicating that a new agent is required to bear a part of the purpose. Isn't it convenient, the idea of being able to specifically "Please take care of this stuff for me". Fire and forget.

```
// "Please take care of OSNotification for me"
const osNotificationWorker = OSNotificationWorker.make();
```

The main point of systemic-ts is to design agents that work well and are easily maintained. The Throwless Pact's absence of `throw`, combined with runtime type validation provides the reliability of agents. The signature transparency of The Throwless Pact aids by quickening the process of understanding agents' essence, and purpose, without having to scrutinize the implementation detail. Last, but not least, closure over class provides a quicker way to iterate while developing and maturing an agent.

In the end, an agent is a system that may reside within another bigger system. It is by principle must not be [scriptic](https://valand.dev/systemic-ts/prelude-1-system-vs-script).

### Agent as Cybernetic Loop

The good news is: JavaScript has a simple yet powerful [async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) that allows modeling concurrent agents. TypeScript completes the static typing part.

But before we dive into the core idea of this article, have you ever seen the pattern below?

```
function doStuffIndefinitely() {
  doStuff();
  setTimeout(doStuffIndefinitely, 100);
}
```

That pattern is a prototype of what I prefer to call the cybernetic loop--this article's core idea.

[Cybernetic](https://en.wikipedia.org/wiki/Cybernetics) is about circular repeating processes. [Norbert Wiener](https://en.wikipedia.org/wiki/Norbert_Wiener) named it _kubernētikēs_ (meaning steering) inspired by the phenomenon where a helmsman's steering behavior is affected by his observation of the effect of his own past steering on the current ship's course.

The helmsman's cybernetic loop is a loop containing the routine of: observe, steer, observe, steer, observe, steer, and so on. Put abstractly, a cybernetic loop contains the routine of its agent.

Let's cut to the chase and convert the above "prototype" code into a loop.

```
const doStuffIndefinitely = async () => {
  while (true) {
    doStuff();
    await sleep(100);
  }
};

// helper
const sleep = (dur: number) => new Promise((res) => setTimeout(res, dur));
```

In a high-level language such as JavaScript, this loop is not as common of a pattern as it is in lower-level languages (e.g. C, C++, Rust). In JavaScript, functionalities that require such a loop have been enabled by [its internal event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop).

However, JavaScript's event loop's capability is limited, so people start to form the loop's "prototype" to make up for the missing features.

The cybernetic loop is a powerful model for long-running processes such as:

*   a game engine's main loop
*   an HTTP server
*   a controller within a pipeline
*   [fiber](https://en.wikipedia.org/wiki/Fiber_(computer_science)) processor.

Let us see how easy to add a feature to a cybernetic loop.

External and internal termination can be added just in several lines.

```
const QuittableAgent = async (externalKillSignal: () => bool) => {
  while (!externalKillSignal()) {
    const res = await work();
    if (res === QUIT) break;
    await sleep(0);
  }
};
```

Adding a state would allow advanced mechanisms such as self-regulation.

```
const SelfRegulatingAgent = async (externalKillSignal: () => bool) => {
  const state = makeState();
  while (!externalKillSignal()) {
    const res = await work(state);
    if (res === QUIT) break;
    await sleep(0);
  }
};
```

Finally, an external could be established by means of an input buffer. Add a bit of an `end`-related feature (e.g. waiting for the agent to shut down).

```
const InteractibleAgent = (externalKillSignal: () => bool) => {
  const input = makeInputBuffer();
  const state = makeState();

  const end = (async () => {
    while (!input.externalKillSignal() && !externalKillSignal()) {
      const res = await work(state, input);
      if (res === QUIT) break;
      await sleep(0);
    }
  })();

  let endFlag = false;
  const isEnded = () => endFlag;

  end.finally(() => (ended = true));

  return { input, end, isEnded };
};
```

The above agent is interactible this way.

```
const agent = InteractibleAgent();
// issue command on agent
await agent.input.someCommand();
// retrieve data from agent
const agent = input.getSomeValue();
// end agent
agent.input.kill();
// wait for the agent to end
await agent.end;
```

Keep note that these forms are simplifications.

For example, `input`, `state`, and `work(state, input)` will be more complex in the real world. `input` for example should be properly typed so that parties that interact with the agent can know the agent's capability.

Another important point is that this pattern naturally leads the programmer to program `input` (or any externally available methods) as a buffer or a cache. This makes the agent more resilient toward mischievous external parties (e.g. if one of the methods is spammed)

### Sub agents

Cybernetic loop pattern is compatible with a hierarchical structure. Let us take an example of a parallel processing hub, a small machine that reroutes requests to other powerful processors. The processors work at different paces so the hub needs to communicate with each processor asynchronously.

```
const Hub = (params: {
  processorsAddresses: string[];
  requestPort: Port;
  offloadPort: Port;
  externalKillSignal: () => bool;
}) => {
  // Generate an agent for each processorsAddresses
  // 'agents' variable is a container of agents with helper
  // methods to find agents of various statuses
  const agents = ProcessorAgents.makeBulk(
    params.processorsAddresses,
    params.externalKillSignal
  );

  while (!params.externalKillSignal()) {
    // Offload done work to offload port
    const doneWorkings = agents.findAwaitingForOffload();
    doneWorkings.forEach((agent) => agent.offloadFrom(params.offloadPort));

    // For each idle agent, supply it with a request
    const readyForWorks = agents.findIdleAgents();
    readyForWorks.forEach((agent) => agent.startWorkFrom(params.requestPort));

    await sleep(500);
  }
};
```

This setup is nice, the hub is not blocked by neither the `Ports` nor the `ProcessorAgents`--no bottlenecks.

It does not have to worry about the `ProcessorAgents` timing because we assume that these processors self-regulate. For example, 1.) they signal their state accurately, whether they are ready to take another request or ready to offload so that `findAwaitingForOffload` and `findIdleAgents` filters the correct agents, or 2.) that malicious calls to `startWorkFrom` or `offloadFrom` are handled well internally.

### Explicit Lifetime Management and Agents

The idea of explicit lifetime management has been briefly visited in the [closure-over-class](https://valand.dev/systemic-ts/systemic-2-closure-over-class), but now let us revisit the idea and relate it to agents and sub-agents.

Unless demanded by exotic requirement, generally and by default the sub-agents must not outlive their parent. This reasoning spans from the top-level or root-level agent to all leaves (if the hierarchical agents are perceived as a tree) so that the root lives the longest and encompasses all agents' lifetimes.

However, since an agent's control flow is detached from its ancestors, each parent is responsible for explicitly stopping its children and waiting for their lifetime to end before ending their own lifetime. Therefore it is necessary for each agent to have a `destroy` method that is only exposed to the parent.

Poetically, the root-level `destroy` "method" of a GUI application is the close (X) button that the user, its parent, can click before the user turns off the PC and continues with life.

### Illusion of Task

Since an agent is long-running and concurrent, it must also be asynchronous in TypeScript/JavaScript world. This notion is not limited to the TypeScript/JavaScript world and is often the primary cause of confusing an agent with a task.

To counter-argue my previous point that "sub-agents" must not outlive their parent, I am tempted to say that nowadays in the cloud-pervasive world, we often spawn a remote agent that works for us while its parent is sleeping. Particularly, I am talking about spawning in-cloud rent computers e.g. AWS, Azure, and Google's virtual machines.

But a computer we issue remotely is not purely an agent of us. In a way, what we do is issue a task to a third-party provider, which is put into practice by spawning an agent of theirs as an agent of ours.

I encourage you to meditate on this phenomenon and put it back in the context of agents within programs, or even within a TypeScript-based program.

**For an entity that could be an agent, could it be represented as a task instead?**

This question is important because agents need explicit lifetime management and manually managing lifetime isn't an easy task. Thus, a program could be modeled as agents passing tasks (and messages in general) to one another. This brings us back to the [first inspiration of OOP](https://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented), but not having to develop a whole new language and falling into the traps such as prematurely [marrying inheritance to the language](https://en.wikipedia.org/wiki/Composition_over_inheritance), or prematurely marrying module visibility with data encapsulation, or deciding that [everything is an object!](https://en.wikipedia.org/wiki/Object-oriented_programming)

### Part 2 — Gang-of-Four Patterns in TypeScript

*by refactoring.guru · conceptual examples adapted for TypeScript*

#### Creational patterns


## Complication 6 No Destructor (P:complication-6-no-destructor)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-6-no-destructor), copyright the author, redistributed with attribution.

Some languages have [destructors](https://en.wikipedia.org/wiki/Destructor_(computer_programming)), but not JavaScript/TypeScript. Some argue that it is unnecessary for scripts.

If you must write a system that juggles around file and socket handles, chances are, you will forget to close some of them. So I argue that it has been necessary even since NodeJS.

```
// https://nodejs.org/api/fs.html#fscreatewritestreampath-options
const writeStream = fs.createWriteStream(somePath, {
  autoClose: false,
});
```

If you open enough of these kind of non-auto-closing streams and forget them, it will cause you "too many open file errors", for example. In a simple script, it is dismissable as a beginner's mistake. In a long-running system, resource leaks can cause contentions (i.e. different parts of the same system competing for a resource) and unnecessary context switches.

By not having a destructor, we cannot tell the runtime to close a file handle, socket handle, and any other side-effect-ish constructs whenever there is no more reference pointing to it.

### Relation to layered lifetime

_Related: [class vs layered lifetime](https://valand.dev/systemic-ts/class-layered-lifetime)_

Destructor not existing correlates with the lifetime management. The common fix to this problem is separating resource owners (e.g. who makes and destroys streams) from resource operators (who pump bytes into the streams).

```
const withStream = async (somePath: string, fns: ((stream: WritableStream) => Promise<unknown>)[]) => {
  // initialize resource
  const writeStream = fs.createWriteStream(somePath, {
    autoClose: false;
  });
  // do whatever you want with it
  await Promise.all(fns.map(() => fn(stream)))
  writeStream.close()
}
```

Separating users from ownership follows a similar pattern as GC.

```
// A total oversimplification!
const SystemWithGC = async () => {
  // initialize resource management system
  const resourceContext = createResourceContext();
  const instructionAndSoOn = createInstructionsQueue();
  while (true) {
    // operate on resource
    await instructionAndSoOn.run(resourceContext, {
      parkAfterInMilliseconds: 500,
    });
    // manage resource
    await resourceContext.markAndSweep();
  }
};
```

_"Can I Copy Your Homework? Yeah just change it up a bit so it doesn't look obvious you copied."_

If you squint your eyes, the pattern looks similar to [data-oriented design](https://en.wikipedia.org/wiki/Data-oriented_design), although it has a different purpose and details.

```
// Another total oversimplification!
const fn = async () => {
  const uniformData1 = [...]
  const uniformData2 = [...]
  const uniformData3 = [...]

  await instruction1(uniformData1)
  await instruction2(uniformData2)
  await instruction3(uniformData3)
}
```

#### Footnote:

_At the time of writing, there are a [proposal](https://github.com/tc39/proposal-explicit-resource-management) and a [solution](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global\_Objects/FinalizationRegistry). The latter is hard to use because of how the rest of the language has been designed. You can tell by the many red warnings that approximately say "Don't touch unless you're absolutely sure."_
